/* Write a program that opens two text files for input and one for
   output.The program should concatenate the corresponding lines of
   the input files, use a space as a separator, and write the results
   to the output file. If one file is shorter than the other, the
   remaining lines in the longer file should also be copied to the
   output file. For example, suppose the first input file has these
   contents:
   eggs kites donuts
   balloons hammers
   stones
   And suppose the second input file has these contents:
   zero lassitude
   finance drama
   The resulting file would have these contents:
   eggs kites donuts zero lassitude
   balloons hammers finance drama
   stones */
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main(int argc, char * argv[])
{
  cout << "Concatenate two files to a new file.\n"
       << "Usage: " << argv[0] << " source_file_1 source_file_2 "
       << "target_file" << endl;
  if ( argc < 4 ) {
    cerr << "ERROR: need 3 argument but only " << argc - 1
         << " given" << endl;
    return -1;
  }
  ifstream fin1(argv[1]);
  if ( ! fin1.is_open() ) {
    cerr << "ERROR: " << argv[1] << " file not found." << endl;
    return -1;
  }
  ifstream fin2(argv[2]);
  if ( ! fin2.is_open() ) {
    cerr << "ERROR: " << argv[1] << " file not found." << endl;
    fin1.close();
    return -1;
  }
  ofstream fout(argv[3]);
  string line1, line2, target;
  while ( getline(fin1, line1) ) {
    if ( getline(fin2, line2) ) {
      target = line1 + " " + line2;
      fout << target << endl;
    }
    else
      fout << line1 << endl;
  }
  while ( getline(fin2, line2) )
    fout << line2 << endl;
  fin1.close();
  fin2.close();
  fout.close();
  cout << "Job done." << endl;
  return 0;
}
