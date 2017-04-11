#Makefile for the prodject FLARM

clean:
	rm *.pyc

test: clean
	@echo "not implemented any tests for now"

run:
	python main.py

help:
	@echo "    clean"
	@echo "        rm *.pyc"
	@echo "    run"
	@echo "        python main.py"
