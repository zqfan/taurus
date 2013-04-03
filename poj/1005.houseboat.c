#include <stdio.h>

void main() {
  int n;
  float x,y,area;
  int year,i;

  scanf("%d", &n);
  for (i = 0; i < n; i++) {
    scanf("%f %f", &x,&y);
    area = 3.1415926*(x*x+y*y)/2;
    year = (int)(area/50 + 1);
    printf("Property %d: This property will begin eroding in year %d.\n",i+1,year);
  }
  printf("END OF OUTPUT.\n");
}
