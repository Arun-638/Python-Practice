#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to check if page is already in frames
int isPresent(int frames[], int frameCount, int page)
{
    for (int i = 0; i < frameCount; i++)
    {
        if (frames[i] == page)
            return 1;
    }
    return 0;
}

// FIFO Page Replacement
int fifo(int pages[], int n, int frameCount)
{
    int frames[10];
    int faults = 0;
    int index = 0;

    for (int i = 0; i < frameCount; i++)
        frames[i] = -1;

    for (int i = 0; i < n; i++)
    {
        if (!isPresent(frames, frameCount, pages[i]))
        {
            frames[index] = pages[i];
            index = (index + 1) % frameCount;
            faults++;
        }
    }

    return faults;
}

// LRU Page Replacement
int lru(int pages[], int n, int frameCount)
{
    int frames[10];
    int recent[10];
    int faults = 0;

    for (int i = 0; i < frameCount; i++)
    {
        frames[i] = -1;
        recent[i] = -1;
    }

    for (int i = 0; i < n; i++)
    {
        int found = 0;

        for (int j = 0; j < frameCount; j++)
        {
            if (frames[j] == pages[i])
            {
                recent[j] = i;
                found = 1;
                break;
            }
        }

        if (!found)
        {
            int lruIndex = 0;

            for (int j = 1; j < frameCount; j++)
            {
                if (recent[j] < recent[lruIndex])
                    lruIndex = j;
            }

            frames[lruIndex] = pages[i];
            recent[lruIndex] = i;
            faults++;
        }
    }

    return faults;
}

// Optimal Page Replacement
int optimal(int pages[], int n, int frameCount)
{
    int frames[10];
    int faults = 0;

    for (int i = 0; i < frameCount; i++)
        frames[i] = -1;

    for (int i = 0; i < n; i++)
    {
        if (isPresent(frames, frameCount, pages[i]))
            continue;

        int replaceIndex = -1;
        int farthest = i + 1;

        // Find empty frame first
        for (int j = 0; j < frameCount; j++)
        {
            if (frames[j] == -1)
            {
                replaceIndex = j;
                break;
            }
        }

        // If no empty frame, find optimal replacement
        if (replaceIndex == -1)
        {
            int maxDistance = -1;

            for (int j = 0; j < frameCount; j++)
            {
                int k;
                for (k = i + 1; k < n; k++)
                {
                    if (frames[j] == pages[k])
                        break;
                }

                if (k == n)
                {
                    replaceIndex = j;
                    break;
                }

                if (k > maxDistance)
                {
                    maxDistance = k;
                    replaceIndex = j;
                }
            }
        }

        frames[replaceIndex] = pages[i];
        faults++;
    }

    return faults;
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: %s <length> <frames>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    int frameCount = atoi(argv[2]);

    if (frameCount < 1 || frameCount > 7)
    {
        printf("Frames must be between 1 and 7\n");
        return 1;
    }

    int pages[100];

    srand(time(0));

    printf("Random Page Reference String:\n");

    for (int i = 0; i < n; i++)
    {
        pages[i] = rand() % 10; // pages 0 to 9
        printf("%d ", pages[i]);
    }

    printf("\n");

    printf("\nFIFO Page Faults    = %d\n", fifo(pages, n, frameCount));
    printf("LRU Page Faults     = %d\n", lru(pages, n, frameCount));
    printf("Optimal Page Faults = %d\n", optimal(pages, n, frameCount));

    return 0;
}