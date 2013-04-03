#include <stdio.h>

void main(void) {
  double balance = 0;
  double total = 0;
  double mean = 0;

  int i;
  for (i = 0; i < 12; i++) {
    scanf("%lf", &balance);
    total += balance;
  }

  mean = total / 12;

  printf("$%.2f\n", mean);
}
