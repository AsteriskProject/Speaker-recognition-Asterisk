CC=gcc
EXEC=binarytest.out

all: $(EXEC)

binarytest: simpleprogram.c
		$(CC) $< -o $(EXEC) 

clean:
		rm $(EXEC)


