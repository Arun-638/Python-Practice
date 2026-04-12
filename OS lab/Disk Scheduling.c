#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 10
#define MAX_CYLINDER 4999

// Sorting function
void sort(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// SSTF Algorithm
int sstf(int req[], int head)
{
    int visited[SIZE] = {0};
    int total = 0;

    for (int i = 0; i < SIZE; i++)
    {
        int min = 5000;
        int index = -1;

        for (int j = 0; j < SIZE; j++)
        {
            if (!visited[j])
            {
                int dist = abs(head - req[j]);
                if (dist < min)
                {
                    min = dist;
                    index = j;
                }
            }
        }

        total += abs(head - req[index]);
        head = req[index];
        visited[index] = 1;
    }

    return total;
}

// LOOK Algorithm
int look(int req[], int head)
{
    int temp[SIZE];
    int total = 0;

    for (int i = 0; i < SIZE; i++)
        temp[i] = req[i];

    sort(temp, SIZE);

    int i;

    // Move right first
    for (i = 0; i < SIZE; i++)
    {
        if (temp[i] >= head)
            break;
    }

    int current = head;

    for (int j = i; j < SIZE; j++)
    {
        total += abs(current - temp[j]);
        current = temp[j];
    }

    for (int j = i - 1; j >= 0; j--)
    {
        total += abs(current - temp[j]);
        current = temp[j];
    }

    return total;
}

// CSCAN Algorithm
int cscan(int req[], int head)
{
    int temp[SIZE];
    int total = 0;

    for (int i = 0; i < SIZE; i++)
        temp[i] = req[i];

    sort(temp, SIZE);

    int i;
    for (i = 0; i < SIZE; i++)
    {
        if (temp[i] >= head)
            break;
    }

    int current = head;

    // Move right
    for (int j = i; j < SIZE; j++)
    {
        total += abs(current - temp[j]);
        current = temp[j];
    }

    // Go to end
    total += abs(current - MAX_CYLINDER);
    current = MAX_CYLINDER;

    // Jump to start
    total += MAX_CYLINDER;
    current = 0;

    // Continue remaining requests
    for (int j = 0; j < i; j++)
    {
        total += abs(current - temp[j]);
        current = temp[j];
    }

    return total;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s <initial_head_position>\n", argv[0]);
        return 1;
    }

    int head = atoi(argv[1]);

    if (head < 0 || head > MAX_CYLINDER)
    {
        printf("Head position must be between 0 and 4999\n");
        return 1;
    }

    int req[SIZE];

    srand(time(0));

    printf("Random Requests:\n");

    for (int i = 0; i < SIZE; i++)
    {
        req[i] = rand() % 5000;
        printf("%d ", req[i]);
    }

    printf("\n");

    printf("\nSSTF Total Head Movement  = %d\n", sstf(req, head));
    printf("LOOK Total Head Movement  = %d\n", look(req, head));
    printf("CSCAN Total Head Movement = %d\n", cscan(req, head));

    return 0;
}