#Makefile for the prodject FLARM

clean:
	rm *.pyc

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

test: clean
	py.test --verbose --color=yes $(TEST_PATH)

run:
	python main.py

all:


help:
	@echo "    clean"
	@echo "        rm *.pyc"
	@echo "    run"
	@echo "        python main.py"
