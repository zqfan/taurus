CC=g++
CFLAGS=-c -Wall
SOURCE=cha.13/13.3.cpp

test: test.o
	$(CC) test.o -o test

test.o: $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o test.o

clean:
	rm *.o test
