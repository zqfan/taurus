/* Write a program that copies one file to another. Have the program
   take the file names from the command line. Have the program report
   if it cannot open a file. */

#include <iostream>
#include <fstream>
using namespace std;

int main(int argc, char * argv[])
{
  if (argc < 3)
    cerr << "ERROR: you should specify source file and target file."
         << endl;
  ifstream fin(argv[1]);
  if (!fin.is_open()) {
    cerr << "ERROR: source file " << argv[1] << "cannot be opened."
         << endl;
    return -1;
  }
  ofstream fout(argv[2]);
  char c;
  while (fin.get(c))
    fout.put(c);
  fin.close();
  fout.close();
  return 0;
}
