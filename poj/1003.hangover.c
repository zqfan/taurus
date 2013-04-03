#include <stdio.h>

void main() {
  // read the input
  float goal, sum;
  scanf("%f", &goal);
  while (goal != 0.00) {
    sum = 0;
    int i;
    for (i = 2;; i++) {
      // it must be 1.0f otherwise 1/i will equal to 0
      sum = sum + 1.0f/i;
      if (sum >= goal) {
	printf("%d card(s)\n",i-1);
	break;
      }
    }
    scanf("%f", &goal);
  }
}
