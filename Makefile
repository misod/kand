#Makefile for the prodject FLARM

clean:
	rm *.pyc

test:
	python testLogging.py

run:
	python main.py

cleanFiles:
	echo > logFiles/packetLog.txt
	echo > logFiles/bigErrorLog.txt
	echo > logFiles/smallErrorLog.txt
	echo > logFiles/simpleLog.txt

help:
	@echo "    clean"
	@echo "        rm *.pyc"
	@echo "    run"
	@echo "        python main.py"
