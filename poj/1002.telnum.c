/* source code for problem 1002 of poj.org
 * @author Fan ZhiQiang
 * @since 2012-06-18
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int comp(const void *a, const void *b) {
  return strcmp((char *)a, (char *)b);
}

void main() {
  const int MAX_TEL_LEN = 100;
  const int TEL_LEN = 9;
  const int HYPHEN_INDEX = 3;
  int count = 0;
  char (*tel_num)[TEL_LEN] = NULL;

  scanf("%d", &count);
  tel_num = (char (*)[TEL_LEN])malloc(sizeof(char)*count*TEL_LEN);

  /* read input line to a tmp string and parse it */ 
  int i,j,k,len;
  char tmp[MAX_TEL_LEN];
  for (i = 0; i < count; i++) {
    scanf("%s",tmp);
    len = strlen(tmp);
    k = 0;
    for (j = 0; j < len; j++) {
      if (k == 3) {
	tel_num[i][k] = '-';
	k++;
      }
      if (tmp[j] != '-') {
	if ('0' <= tmp[j] && tmp[j] <= '9')
	  tel_num[i][k] = tmp[j];
	else if ('A' <= tmp[j] && tmp[j] < 'Q')
	  tel_num[i][k] = (tmp[j] - 'A')/3 + 2 + '0';
	else if ('R' <= tmp[j] && tmp[j] <= 'Y')
	  tel_num[i][k] = (tmp[j] - 'A' -1)/3 + 2 + '0';
	k++;
      }
    }
    tel_num[i][k] = '\0';
  }

  qsort(tel_num, count, sizeof(char)*TEL_LEN,comp);

  /* find duplicates */
  int no_dup = 1;
  int dup;
  for (i = 0; i < count; ) {
    dup = 1;
    for (j = i+1; j < count; j++) {
      if (strcmp(tel_num[i], tel_num[j]) == 0) {
	dup++;
	no_dup = 0;
      }
      else
	break;
    }
    if (dup > 1)
      printf("%s %d\n", tel_num[i], dup);
    i = j;
  }
  if (no_dup == 1)
    printf("No duplicates.\n"); 

  free(tel_num);
}
