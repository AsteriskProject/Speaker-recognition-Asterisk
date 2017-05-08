CC=gcc
EXEC=binarytest.out

all: $(EXEC)

binarytest.out: simpleprogram.c
		$(CC) $< -o $(EXEC) 
copy:
	cp "/home/roothome/Speaker-recognition-Asterisk/speechsender.py" "/var/lib/asterisk/agi-bin"
clean:
		rm $(EXEC)


