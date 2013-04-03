#include <stdio.h>

/* @param
 * top: sub tree root node */
void min_heap(int * arr, int top, int length) {
    if (top >= length)
        return;
    int top_value = arr[top];
    int child = 2 * top + 1;
    while (child < length) {
        if (child + 1 < length) {
            if (arr[child] > arr[child+1])
                child += 1;
        }
        if (top_value > arr[child]) {
            arr[top] = arr[child];
            arr[child] = top_value;
            top = child;
            child = 2 * top + 1;
        } else
            break;
    }
}

void heap_sort(int * arr, int length, int asce) {
    int i;
    for (i = length/2; i >= 0; i--)
        min_heap(arr, i, length);
    int min;
    for (i = length-1; i >= 1; i--) {
        min = arr[0];
        arr[0] = arr[i];
        arr[i] = min;
        min_heap(arr, 0, i);
    }
}

/* find the biggest in unordered area,
 * swap with first one in unordered area */
void select_sort(int * arr, int length, int asce) {
    int i,j,k,tmp;
    for (i = 0; i < length; i++) {
        tmp = arr[i];
        for (j = i+1; j < length; j++) {
            if (arr[j] < tmp) {
                tmp = arr[j];
                k = j;
            }
        }
        if (arr[i] > tmp) {
            arr[k] = arr[i];
            arr[i] = tmp;
        }
    }
}

void insert_sort(int * arr, int length, int asce) {
    int i,j,k,tmp;
    for (i = 1; i < length; i++) {
        tmp = arr[i];
        for ( j = 0; j < i; j++ ) {
            if ((asce==1) && (tmp < arr[j]))
	            break;
            else if ((asce==0) && (tmp > arr[j]))
	            break;
        }
        for (k = i - 1; k >= j; k--)
            arr[k+1] = arr[k];
        arr[j] = tmp;
    }
}

/* swap adjoining position for bubble
 * each circle put the biggest in the end of the unsorted area */
void bubble_sort(int * arr, int length, int asce) {
    int i,j,tmp;
    for (i = length - 1; i >= 1; i--) {
        for (j = 0; j < i; j++) {
            if ((asce == 1) && (arr[j] > arr[j+1])) {
	            tmp = arr[j+1];
	            arr[j+1] = arr[j];
	            arr[j] = tmp;
            } else if ((asce == 0) && (arr[j] < arr[j+1])) {
	            tmp = arr[j+1];
	            arr[j+1] = arr[j];
	            arr[j] = tmp;
            }
        }
    }
}

void main(void) {
  int arr[10]={9,8,70,6,5,4,3,2,1,0};
  heap_sort(arr,10,1);
  int i;
  for (i = 0; i < 10; i++)
    printf("%d ",arr[i]);
}
