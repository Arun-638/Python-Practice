#include <stdio.h>

#define MAX_PROCESSES 10
#define MAX_RESOURCES 10

int main() {
    int n, m;

    int available[MAX_RESOURCES];
    int allocation[MAX_PROCESSES][MAX_RESOURCES];
    int request[MAX_PROCESSES][MAX_RESOURCES];

    int finish[MAX_PROCESSES];
    int work[MAX_RESOURCES];

    printf("Enter number of processes: ");
    scanf("%d", &n);

    printf("Enter number of resources: ");
    scanf("%d", &m);

    printf("Enter Available resources:\n");
    for(int i = 0; i < m; i++)
        scanf("%d", &available[i]);

    printf("Enter Allocation Matrix:\n");
    for(int i = 0; i < n; i++)
        for(int j = 0; j < m; j++)
            scanf("%d", &allocation[i][j]);

    printf("Enter Request Matrix:\n");
    for(int i = 0; i < n; i++)
        for(int j = 0; j < m; j++)
            scanf("%d", &request[i][j]);
    for(int i = 0; i < m; i++)
        work[i] = available[i];

    for(int i = 0; i < n; i++) {
        int zeroAllocation = 1;
        for(int j = 0; j < m; j++) {
            if(allocation[i][j] != 0) {
                zeroAllocation = 0;
                break;
            }
        }

        if(zeroAllocation)
            finish[i] = 1;
        else
            finish[i] = 0;
    int found;

    do {
        found = 0;

        for(int i = 0; i < n; i++) {

            if(finish[i] == 0) {

                int possible = 1;

                for(int j = 0; j < m; j++) {
                    if(request[i][j] > work[j]) {
                        possible = 0;
                        break;
                    }
                }

                if(possible) {
                    for(int j = 0; j < m; j++)
                        work[j] += allocation[i][j];

                    finish[i] = 1;
                    found = 1;
                }
            }
        }

    } while(found);
    int deadlock = 0;

    for(int i = 0; i < n; i++) {
        if(finish[i] == 0) {
            deadlock = 1;
            break;
        }
    }

    if(deadlock == 0) {
        printf("\nSystem is NOT Deadlocked.\n");
    } else {
        printf("\nSystem is Deadlocked.\nDeadlocked Processes: ");
        for(int i = 0; i < n; i++) {
            if(finish[i] == 0)
                printf("P%d ", i);
        }
        printf("\n");
    }

    
}
return 0;
}