#include "quicksort.h"

void swap(int* a, int* b) 
{ 
    int t = *a; 
    *a = *b; 
    *b = t; 
} 

unsigned partition(int* a, unsigned left, unsigned right) {
   int i = left;
   int pivot = a[right];
   for(unsigned j = left; j < right; ++j) {
       if (a[j] < pivot) {
           swap(&a[j], &a[i]);
           ++i;
       }
   }
   swap(&a[i], &a[right]);
   return i;
}

void quicksort(int* a, unsigned left, unsigned right) {
    unsigned pivot = partition(a, left, right);
    if (pivot > left + 1)
        quicksort(a, left, pivot - 1);
    if (right > pivot + 1)
        quicksort(a, pivot + 1, right);
}
