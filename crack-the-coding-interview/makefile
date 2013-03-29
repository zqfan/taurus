CC=g++
CFLAGS=-c -Wall
SOURCE=cha.9/9.1.c

test: link.o test.o
	$(CC) link.o test.o -o test

test.o: $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o test.o

link.o: link.c
	$(CC) $(CFLAGS) link.c

clean:
	rm *.o test
