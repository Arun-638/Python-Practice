#include<stdio.h>
#include<unistd.h>
#include<string.h>
#include<sys/msg.h>
#include<sys/ipc.h>
struct message{
    long msg_type;
    char msg_text[100];
};
int main(){
    int msgid;
    struct message msg;
    msgid = msgget(1234,0666|IPC_CREAT);
    pid_t pid = fork();
    if(pid < 0){
        printf("Fork Failed\n");
        return 1;
    }
    else if (pid == 0){
        msgrcv(msgid,&msg,sizeof(msg),1,0);
        printf("Received Message: %s\n", msg.msg_text);
        int size = strlen(msg.msg_text);
        for(int i=0;i<size/2;i++){
            char temp = msg.msg_text[i];
            msg.msg_text[i] = msg.msg_text[size-i-1];
            msg.msg_text[size-i-1] = temp;
        }
        msg.msg_type = 2;
        msgsnd(msgid,&msg,sizeof(msg),0);
    }
    else{
        msg.msg_type = 1;
        printf("Enter a message: ");
        scanf("%s",msg.msg_text);
        char original[100];
        strcpy(original,msg.msg_text);
        msgsnd(msgid,&msg,sizeof(msg),0);
        msgrcv(msgid,&msg,sizeof(msg),2,0);
        printf("Original Message: %s\n", original);
        printf("Reversed Message: %s\n", msg.msg_text);
        if (strcmp(original,msg.msg_text) == 0){
            printf("The original and reversed messages are the same.\n");
        }
        else{
            printf("The original and reversed messages are different.\n");
        }
    }
    return 0;
}