#Makefile for the prodject FLARM

clean:
	rm *.pyc

test:
	python testLogging.py

run:
	python main.py

help:
	@echo "    clean"
	@echo "        rm *.pyc"
	@echo "    run"
	@echo "        python main.py"
