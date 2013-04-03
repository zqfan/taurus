/* Write a program that copies your keyboard input (up to the
   simulated end-of-file) to a file named on the command line. */

#include <iostream>
#include <fstream>
using namespace std;

int main(int argc, char * argv[])
{
  if (argc < 2)
    cerr << "ERROR: you should specify a filename" << endl;
  ofstream fout(argv[1]);
  char c;
  while (cin.get(c))
    fout.put(c);
  fout.close();
  return 0;
}
