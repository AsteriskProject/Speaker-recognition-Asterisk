CC=gcc
EXEC=binarytest.out
NAMEPROGPYTHON=speechsender.py
all: $(EXEC)

binarytest.out: simpleprogram.c
		$(CC) $< -o $(EXEC) 
copy:
	chmod a+x $(NAMEPROGPYTHON) 
	cp "./$(NAMEPROGPYTHON)" "/var/lib/asterisk/agi-bin"
dialplan:
	cp "./extensions_custom.conf" "/etc/asterisk/"
clean:
	rm $(EXEC)


