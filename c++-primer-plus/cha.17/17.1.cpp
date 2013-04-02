/* 1.
   Write a program that counts the number of characters up to the
   first $ in input and that leaves the $ in the input stream.
*/
#include <iostream>
using namespace std;

int main()
{
  int count = 0;
  char c = '\0';
  cout << "this program will count the number of characters up to "
       << "the first $\nif the string doesn't contain $, use CTRL+D "
       << "to quit, ENTER will be counted so it cannot quit.\n"
       << "input your string:" << endl;
  while ( cin.get(c) && c != '$' )
    count++;
  if ( c == '$' )
    cin.putback(c);
  cout << "character count = " << count << endl;
  return 0;
}
