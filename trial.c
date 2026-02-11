#include <stdio.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <ctype.h>

int main() {
    int shmid = shmget(1234, 1024, 0666 | IPC_CREAT);
    char *data = (char *)shmat(shmid, NULL, 0);
    pid_t pid = fork();
    if (pid == 0) {
        char result[200];
        char s1[50], s2[50], s3[50];
        sscanf(data, "%s %s %s", s1, s2, s3);
        sprintf(result, "%s %s %s", s1, s2, s3);
        strcpy(data, result);
    } else {
        printf("Enter three strings separated by spaces: ");
        fgets(data, 1024, stdin);
        sleep(1);
        for (int i = 0; data[i]; i++) {
            if (islower(data[i]))
                data[i] = toupper(data[i]);
            else if (isupper(data[i]))
                data[i] = tolower(data[i]);
        }
        printf("Output: %s\n", data);
        shmdt(data);
    }
    return 0;
}
