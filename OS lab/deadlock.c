#include <stdio.h>
#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int main() {
    int n, m;

    int available[MAX_RESOURCES];
    int max[MAX_PROCESSES][MAX_RESOURCES];
    int allocation[MAX_PROCESSES][MAX_RESOURCES];
    int need[MAX_PROCESSES][MAX_RESOURCES];

    int finish[MAX_PROCESSES] = {0};
    int safeSeq[MAX_PROCESSES];

    printf("Enter number of processes: ");
    scanf("%d", &n);

    printf("Enter number of resources: ");
    scanf("%d", &m);

    printf("Enter available resources:\n");
    for(int i = 0; i < m; i++)
        scanf("%d", &available[i]);

    printf("Enter Allocation Matrix:\n");
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            scanf("%d", &allocation[i][j]);
        }
    }

    printf("Enter Maximum Matrix:\n");
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            scanf("%d", &max[i][j]);
        }
    }
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < m; j++) {
            need[i][j] = max[i][j] - allocation[i][j];
        }
    }

    int count = 0;

    while(count < n) {
        int found = 0;

        for(int i = 0; i < n; i++) {

            if(finish[i] == 0) {

                int possible = 1;

                for(int j = 0; j < m; j++) {
                    if(need[i][j] > available[j]) {
                        possible = 0;
                        break;
                    }
                }

                if(possible) {
                    for(int j = 0; j < m; j++) {
                        available[j] += allocation[i][j];
                    }

                    safeSeq[count++] = i;
                    finish[i] = 1;
                    found = 1;
                }
            }
        }
        if(found == 0) {
            printf("\nSystem is NOT in Safe State.\n");
            return 0;
        }
    }

    printf("\nSystem is in SAFE State.\nSafe Sequence:\n");

    for(int i = 0; i < n; i++)
        printf("P%d ", safeSeq[i]+1);

    printf("\n");

    return 0;
}