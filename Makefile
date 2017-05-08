CC=gcc
EXEC=binarytest.out

all: $(EXEC)

binarytest.out: simpleprogram.c
		$(CC) $< -o $(EXEC) 
copy:
	cp "/home/roothome/Speaker-recognition-Asterisk/binarytest.out" "/var/lib/asterisk/agi-bin/binarytest.out"
clean:
		rm $(EXEC)


