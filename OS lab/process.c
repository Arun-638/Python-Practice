#include <stdio.h>
#include <limits.h>

#define MAX 10
#define Q 3

int n;
int pid[MAX], bt[MAX], at[MAX], pr[MAX];
int ct[MAX], tat[MAX], wt[MAX];
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

/* Sort by Arrival Time (for FCFS) */
void sort_by_arrival() {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (at[j] > at[j + 1]) {
                swap(&at[j], &at[j + 1]);
                swap(&bt[j], &bt[j + 1]);
                swap(&pid[j], &pid[j + 1]);
                swap(&pr[j], &pr[j + 1]);
            }
        }
    }
}
/* ---------- FCFS ---------- */
double fcfs() {
    sort_by_arrival();
    int time = 0, total = 0;

    for (int i = 0; i < n; i++) {
        if (time < at[i])
            time = at[i];

        time += bt[i];
        ct[i] = time;

        tat[i] = ct[i] - at[i];
        wt[i]  = tat[i] - bt[i];

        total += wt[i];
    }
    return (double)total / n;
}

/* ---------- SRTF ---------- */
double srtf() {
    int rt[MAX];
    int time = 0, completed = 0, total = 0;

    for (int i = 0; i < n; i++)
        rt[i] = bt[i];

    while (completed < n) {
        int idx = -1, min = INT_MAX;

        for (int i = 0; i < n; i++) {
            if (at[i] <= time && rt[i] > 0 && rt[i] < min) {
                min = rt[i];
                idx = i;
            }
        }

        if (idx == -1) {
            time++;
            continue;
        }

        rt[idx]--;
        time++;

        if (rt[idx] == 0) {
            ct[idx] = time;
            tat[idx] = ct[idx] - at[idx];
            wt[idx]  = tat[idx] - bt[idx];

            total += wt[idx];
            completed++;
        }
    }
    return (double)total / n;
}

/* ---------- Priority (Non-preemptive) ---------- */
double priority() {
    int done[MAX] = {0};
    int time = 0, completed = 0, total = 0;

    while (completed < n) {
        int idx = -1, maxp = -1;

        for (int i = 0; i < n; i++) {
            if (at[i] <= time && !done[i] && pr[i] > maxp) {
                maxp = pr[i];
                idx = i;
            }
        }

        if (idx == -1) {
            time++;
            continue;
        }

        time += bt[idx];
        ct[idx] = time;

        tat[idx] = ct[idx] - at[idx];
        wt[idx]  = tat[idx] - bt[idx];

        total += wt[idx];
        done[idx] = 1;
        completed++;
    }
    return (double)total / n;
}

/* ---------- Round Robin ---------- */
double round_robin() {
    int rt[MAX];
    int time = 0, completed = 0, total = 0;

    for (int i = 0; i < n; i++)
        rt[i] = bt[i];

    while (completed < n) {
        for (int i = 0; i < n; i++) {
            if (at[i] <= time && rt[i] > 0) {
                if (rt[i] > Q) {
                    time += Q;
                    rt[i] -= Q;
                } else {
                    time += rt[i];
                    rt[i] = 0;

                    ct[i] = time;
                    tat[i] = ct[i] - at[i];
                    wt[i]  = tat[i] - bt[i];

                    total += wt[i];
                    completed++;
                }
            }
        }
    }
    return (double)total / n;
}

/* ---------- MAIN ---------- */
int main() {
    printf("Enter number of processes: ");
    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        printf("PID BT AT Priority: ");
        scanf("%d %d %d %d", &pid[i], &bt[i], &at[i], &pr[i]);
    }

    double a = fcfs();
    double b = srtf();
    double c = priority();
    double d = round_robin();

    printf("\nAverage Waiting Time\n");
    printf("FCFS     : %.2f\n", a);
    printf("SRTF     : %.2f\n", b);
    printf("Priority : %.2f\n", c);
    printf("RR       : %.2f\n", d);

    return 0;
}
