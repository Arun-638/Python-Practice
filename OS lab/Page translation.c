#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int virtualspace, pagesize, virtualaddress;
    int pagenumber, offset, framenumber;

    if (argc > 3)
    {
        // Taking input from command line
        virtualspace = atoi(argv[1]);      // in MB
        pagesize = atoi(argv[2]);          // in KB
        virtualaddress = atoi(argv[3]);    // address value

        // Convert MB to bytes
        virtualspace = virtualspace * 1024 * 1024;

        // Convert KB to bytes
        pagesize = pagesize * 1024;

        // Total number of pages
        int numberofpages = virtualspace / pagesize;

        // Find page number and offset
        pagenumber = virtualaddress / pagesize;
        offset = virtualaddress % pagesize;

        // Create page table
        int pagetable[numberofpages];

        // Fill page table (page i -> frame i)
        for (int i = 0; i < numberofpages; i++)
        {
            pagetable[i] = i;
        }

        // Check page table miss
        if (pagenumber >= numberofpages)
        {
            printf("Page Table Miss!!\n");
            return 0;
        }

        framenumber = pagetable[pagenumber];

        printf("Frame Number = %d\n", framenumber);
        printf("Page Number = %d\n", pagenumber);
        printf("Offset = %d\n", offset);
        printf("Physical Address = <%d, %d>\n", framenumber, offset);
    }
    else
    {
        printf("Invalid format\n");
        printf("Usage: ./a.out <virtualspace(MB)> <pagesize(KB)> <virtualaddress>\n");
    }

    return 0;
}