#include<stdio.h>
#include<unistd.h>
#include<sys/wait.h>
int main(){
    pid_t pid;
    pid = fork();
    if(pid < 0){
        printf("Fork Failed\n");
    }
    else if(pid == 0){
        printf("PCCSL407 ");
    }
    else{
        wait(NULL);
        printf("OS Lab\n");
    }
    return 0;
}