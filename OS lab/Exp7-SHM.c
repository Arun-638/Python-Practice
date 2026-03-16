#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<sys/shm.h>
#include<sys/ipc.h>
#include<sys/wait.h>
#include<ctype.h>
int main(){
    char s1[20],s2[20],s3[20];
    int shmid = shmget(1234,1024,0666|IPC_CREAT);
    char *data = (char*) shmat(shmid,NULL,0);
    printf("Enter First message: ");
    scanf("%s",s1);
    printf("Enter Second message: ");
    scanf("%s",s2);
    printf("Enter Third message: ");
    scanf("%s",s3);
    pid_t pid = fork();
    if(pid < 0){
        perror("Fork Failed\n");
        return 1;
    }
    else if (pid == 0){
        char result[100];
        sprintf(result,"%s %s %s",s1,s2,s3);
        strcpy(data,result);
        shmdt(data);
    }
    else{
        wait(NULL);
        for(int i=0;data[i];i++){
            if(islower(data[i])){
                data[i] = toupper(data[i]);
            }
            else if(isupper(data[i])){
                data[i] = tolower(data[i]);
            }
        }
        printf("Modified Message: %s\n",data);
        shmdt(data);
        shmctl(shmid,IPC_RMID,NULL);
    }
    return 0;
}