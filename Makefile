CC=gcc
EXEC=binarytest

all: $(EXEC)

binarytest: simpleprogram.c
		$(CC) $< -o binarytest 

clean:
		rm $(EXEC)


