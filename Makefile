CC=gcc
EXEC=binarytest.out

all: $(EXEC)

binarytest.out: simpleprogram.c
		$(CC) $< -o $(EXEC) 

clean:
		rm $(EXEC)


