CC=g++
CFLAGS=-c -Wall
SOURCE=cha.9/9.1.c

test: test.o
	$(CC) test.o -o test

test.o: $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o test.o

clean:
	rm *.o test
