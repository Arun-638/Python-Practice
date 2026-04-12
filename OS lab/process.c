#include<stdio.h>
#include<string.h>
#define Q 3
#define MAX 10
int n;
int pid[MAX],bt[MAX],at[MAX],pr[MAX];
int ct[MAX],tat[MAX],wt[MAX];
void swap(int *a,int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}
void SortByArrival(){
    for(int i=0;i<n-1;i++){
        for(int j=0;j<n-i-1;j++){
            if(at[j]>at[j+1]){
                swap(&at[j],&at[j+1]);
                swap(&bt[j],&bt[j+1]);
                swap(&pid[j],&pid[j+1]);
                swap(&pr[j],&pr[j+1]);
            }
        }
    }
}
double fcfs(){
    SortByArrival();
    int time = 0,total = 0;
    for(int i=0;i<n;i++){
        if(time<at[i]){
            time = at[i];
        }
        time+=bt[i];
        ct[i] = time;
        tat[i] = ct[i]-at[i];
        wt[i] = tat[i]-bt[i];
        total+=wt[i];
    }
    return (double)total/n;
}
double srtf(){
    int time = 0,total = 0,completed = 0;
    int rt[MAX];
    SortByArrival();
    for(int i =0;i<n;i++){
        rt[i] = bt[i];
    }
    while(completed<n){
        int idx = -1,min = 999;
        for(int i=0;i<n;i++){
            if(at[i]<=time && rt[i]>0 && rt[i]<min){
                min = rt[i];
                idx = i;
            }
        }
        if(idx == -1){
            time++;
            continue;
        }
        time++;   
        rt[idx]--;
        if (rt[idx]==0){
            completed++;
            ct[idx] = time;
            tat[idx] = ct[idx]-at[idx];
            wt[idx] = tat[idx]-bt[idx];
            total+=wt[idx];
        }
    }
    return (double)total/n;
}

double priority(){
    int time = 0,total = 0,completed = 0;
    int done[MAX] = {0};
    SortByArrival();
    while (completed < n){
        int idx = -1,maxp = -1;
        for(int i=0;i<n;i++){
            if(at[i]<=time && !done[i] && pr[i]>maxp){
                maxp = pr[i];
                idx = i;
            }
        }
        if(idx == -1){
            time++;
            continue;
        }
        time+=bt[idx];
        done[idx] = 1;
        completed++;
        ct[idx] = time;
        tat[idx] = ct[idx]-at[idx];
        wt[idx] = tat[idx]-bt[idx];
        total+=wt[idx];
    }
    return (double)total/n;
}

double RR(){
    int time = 0, completed = 0, total = 0;
    int rt[MAX];
    SortByArrival();
    for(int i=0;i<n;i++){
        rt[i] = bt[i];
    }

    int i = 0;

    while(completed < n){

        if(at[i] <= time && rt[i] > 0){

            if(rt[i] > Q){
                time += Q;
                rt[i] -= Q;
            }
            else{
                time += rt[i];
                rt[i] = 0;
                completed++;

                ct[i] = time;
                tat[i] = ct[i] - at[i];
                wt[i] = tat[i] - bt[i];

                total += wt[i];
            }
        }
        i = (i + 1) % n;
        if(i == 0 && time < at[0])  
            time++;
    }

    return (double)total/n;
}
int main(){
    printf("Enter the number of processes: ");
    scanf("%d",&n);
    for(int i=0;i<n;i++){
        printf("Enter PID, Burst Time, Arrival Time and Priority of process %d: ",i+1);
        scanf("%d %d %d %d",&pid[i],&bt[i],&at[i],&pr[i]);
    }
    printf("FCFS Average Waiting Time: %lf\n",fcfs());
    printf("SRTF Average Waiting Time: %lf\n",srtf());
    printf("Priority Average Waiting Time: %lf\n",priority());
    printf("Round Robin Average Waiting Time: %lf\n",RR());
    return 0;
}