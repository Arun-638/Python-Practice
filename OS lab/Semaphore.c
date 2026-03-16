#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

sem_t mutex, wrt, readTry, mutex2;
int readcount = 0;
int writecount = 0;

void *reader(void *arg) {
    int id = *(int *)arg;

    sem_wait(&readTry);
    sem_wait(&mutex);

    readcount++;
    if (readcount == 1)
        sem_wait(&wrt);

    sem_post(&mutex);
    sem_post(&readTry);

    printf("Reader %d is reading\n", id);
    sleep(1);

    sem_wait(&mutex);
    readcount--;
    if (readcount == 0)
        sem_post(&wrt);
    sem_post(&mutex);

    return NULL;
}

void *writer(void *arg) {
    int id = *(int *)arg;

    sem_wait(&mutex2);
    writecount++;
    if (writecount == 1)
        sem_wait(&readTry);
    sem_post(&mutex2);

    sem_wait(&wrt);

    printf("Writer %d is writing\n", id);
    sleep(1);

    sem_post(&wrt);

    sem_wait(&mutex2);
    writecount--;
    if (writecount == 0)
        sem_post(&readTry);
    sem_post(&mutex2);

    return NULL;
}

int main() {
    int r, w;

    printf("Enter number of readers: ");
    scanf("%d", &r);

    printf("Enter number of writers: ");
    scanf("%d", &w);

    pthread_t readers[r], writers[w];
    int rid[r], wid[w];

    sem_init(&mutex, 0, 1);
    sem_init(&wrt, 0, 1);
    sem_init(&readTry, 0, 1);
    sem_init(&mutex2, 0, 1);

    for (int i = 0; i < r; i++) {
        rid[i] = i + 1;
        pthread_create(&readers[i], NULL, reader, &rid[i]);
    }
     
    for (int i = 0; i < w; i++) {
        wid[i] = i + 1;
        pthread_create(&writers[i], NULL, writer, &wid[i]);
    }

    for (int i = 0; i < r; i++)
        pthread_join(readers[i], NULL);

    for (int i = 0; i < w; i++)
        pthread_join(writers[i], NULL);

    printf("Finished execution\n");

    return 0;
}