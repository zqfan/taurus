/* Write a program that requests an integer and then displays it in
   decimal, octal, and hexadecimal forms. Display each form on the
   same line, in fields that are 15 characters wide, and use the C++
   number base prefixes.
*/
#include <iostream>
#include <iomanip>
using namespace std;

int main()
{
  int i;
  cout << "Input your number:" << endl;
  cin >> i;
  cout.setf(ios_base::showbase);
  cout << setw(15) << i
       << setw(15) << oct << i
       << setw(15) << hex << i << endl;
  return 0;
}
