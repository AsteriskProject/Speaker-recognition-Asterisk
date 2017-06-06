CC=gcc
EXEC=binarytest.out
NAMEPROGPYTHON=speechsender.py
PATH_AGI="/var/lib/asterisk/agi-bin

all: $(EXEC)

binarytest.out: simpleprogram.c
		$(CC) $< -o $(EXEC) 
copy:
	cp "./$(NAMEPROGPYTHON)" $(PATH_AGI)	
	chmod a+x $(PATH_AGI)/$(NAMEPROGPYTHON) 
dialplan:
	cp "./extensions_custom.conf" "/etc/asterisk/"
clean:
	rm $(EXEC)


