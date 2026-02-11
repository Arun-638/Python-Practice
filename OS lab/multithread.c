// Write a multithreaded program that calculates the mean, median, and standard deviation for a list of integers. This program should receive a series of integers on the command line and will then create three separate worker threads. The first thread will determine the mean value, the second will determine the median and the third will calculate the standard deviation of the integers. The variables representing the mean, median, and standard deviation values will be stored globally. The worker threads will set these values, and the parent thread will output the values once the workers have exited.
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

int n;
int arr[100];
double mean, median, stddev;

void* find_mean(void* arg) {
    int sum = 0;
    for (int i = 0; i < n; i++)
        sum += arr[i];
    mean = (double)sum / n;
    pthread_exit(NULL);
}

void* find_median(void* arg) {
    int temp;
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (arr[i] > arr[j]) {
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }

    if (n % 2 == 0)
        median = (arr[n/2 - 1] + arr[n/2]) / 2.0;
    else
        median = arr[n/2];

    pthread_exit(NULL);
}

void* find_stddev(void* arg) {
    double sum = 0;
    for (int i = 0; i < n; i++)
        sum += (arr[i] - mean) * (arr[i] - mean);

    stddev = sqrt(sum / n);
    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {

    if (argc < 2) {
        printf("Usage: %s numbers...\n", argv[0]);
        return 0;
    }

    n = argc - 1;
    for (int i = 0; i < n; i++)
        arr[i] = atoi(argv[i + 1]);

    pthread_t t1, t2, t3;

    pthread_create(&t1, NULL, find_mean, NULL);
    pthread_join(t1, NULL);

    pthread_create(&t2, NULL, find_median, NULL);
    pthread_join(t2, NULL);

    pthread_create(&t3, NULL, find_stddev, NULL);
    pthread_join(t3, NULL);

    printf("Mean = %.2f\n", mean);
    printf("Median = %.2f\n", median);
    printf("Standard Deviation = %.2f\n", stddev);

    return 0;
}
