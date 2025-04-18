#include <stdio.h>
#include <omp.h>

int main(void) {
    int nthreads, tid;

    #pragma omp parallel private(tid)
    {
        tid = omp_get_thread_num();
        printf("Hello from thread %d of ?.\n", tid);

        #pragma omp barrier

        if (tid == 0) {
            nthreads = omp_get_num_threads();
            printf("Numero total de hilos = %d\n", nthreads);
        }
    }
    return 0;
}