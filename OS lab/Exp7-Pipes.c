#include<stdio.h>
#include<unistd.h>
#include<math.h>
int main(){
    int fd[2];
    int a,b,c,x,y;
    printf("Enter a b c: ");
    scanf("%d %d %d",&a,&b,&c);
    if(pipe(fd) == -1){
        printf("Pipe Failed\n");
        return 1;
    }
    pid_t pid = fork();
    if(pid < 0){
        printf("Fork Failed\n");
        return 1;
    }
    else if(pid == 0){
        close(fd[0]);
        y = 4*a*c;
        write(fd[1],&y,sizeof(y));
        close(fd[1]);
    }
    else{
        close(fd[1]);
        x = b*b;
        read(fd[0],&y,sizeof(y));
        close(fd[0]);
        printf("Discriminant: %d\n",sqrt((x-y)));
    }
}