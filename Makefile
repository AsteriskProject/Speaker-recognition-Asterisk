CC=gcc
#EXEC=binarytest.out used to test before we had the real binary
NAMEPROGPYTHON=speechsender.py
PATH_AGI=/var/lib/asterisk/agi-bin

copy:
	cp "./$(NAMEPROGPYTHON)" "$(PATH_AGI)"	
	chmod a+x "$(PATH_AGI)/$(NAMEPROGPYTHON)"	
dialplan:
	cp "./extensions_custom.conf" "/etc/asterisk/"
reboot:
	asterisk -rx "core restart now"
logs:
	asterisk -rvvvvv
#clean:
#	rm $(EXEC)


