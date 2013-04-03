/* source code for 1001 exponentiation @ poj.org
 * author ZhiQiang Fan
 * since 2012-06-18
 */
#include <stdio.h>

/* pre-condition:
 * [1] a, b store float numbers to be added
 * [2] length of result must larger than or equal to the max length of a & b
 * [3] result is filled with '0'
 * post-condition:
 * the result is stored int string result
 */
int add(char * a, char * b, char * result) {
  int i,j,k,carry;
  i = strlen(a) - 1;
  j = strlen(b) - 1;
  k = strlen(result) - 1;
  carry = 0;
  for ( ; i >=0 && j >= 0 && k >= 0; i--, j--, k--) {
    result[k] = (a[i] + a[j] - '0'*2)%10 + carry;
    carry = (a[i] + a[j] - '0'*2)/10;
  }
}

/* pre-condition:
 * [1] a, b store float numbers to be added
 * [2] length of result must be enough
 * let digit count of a equals to x, digit count of b equals to y
 * to be safe, length of result must not less than x+y+1
 * post-condition:
 * the result is stored int string result
 */
int mutiply(char * a, char * b, char * result) {
  int i,j,k;
 
}

/* pre-condition:
 * [1] x store a float with a decimal point, it's length must be 6 
 * and if not, it must be filled with '0'
 * [2] 0 < n <= 25
 * [3] the length of result must larger than 5*25+2=127
 * post-condition:
 * the result of x^n is stored in result string
 * informally:
 * this function simulate the manual computation process
 */
int expon_float_string(char * x, int n, char * result) {
  int i;
  int len = strlen(result);
  char * tmp = (char *)malloc(sizeof(char)*len+1);
  for (i = 0; i < len; i++)
    tmp[i] = '0';
  tmp[i] = '\0';
  add(x, tmp, tmp);
  for (i = 1; i < n; i++) {
    multiply(tmp, x, result);
    strcpy(tmp, result);
  }
  free(tmp);
  return 0;
}

/* pre-condition:
 * result stored a float 
 * post-contidion:
 * remove leading zero and useless zero, if result is a integer, 
 * remove the decimal point
 */
int format_float_string(char * result) {
  int len = strlen(result);
  char * tmp = (char *)malloc(sizeof(char)*len+1);
  /* remove leading zero */
  int i = 0;
  while (result[i] == '0')
    i++;
  strcpy(tmp, reslut+i);
  /* remove useless zero */
  int j;
  for (j = len - 1 - i; j > 0 && tmp[j] == '0'; j--)
    tmp[j] = '\0';
  /* remove decimal point if result is a integer */
  if (tmp[j] == '.')
    tmp[j] = '\0';
  return 0;
}

void main() {
  const int INPUT_LEN = 6;
  char x[INPUT_LEN+1]; // the input float number
  int n;
  const int MAX_LEN = 125;
  char result[MAX_LEN+2];
  int dot; // dot index in x, if not exist, dot = -1
  int i;

  while (scanf("%s %d",r,&n) != EOF) {
    for (i = 0; i < (MAX_LEN + 1); i++ ) {
      result[i] = '0';
    }
    result[i] = '\0';

    for (i = 0; i < INPUT_LEN; i++ ) {
      if ('.' == r[i]) {
	dot = i;
	break;
      }
    }
    expon_float_string(x, n, result);
    fomart_float_string(result);
    printf("%s\n", result);
  }
}
