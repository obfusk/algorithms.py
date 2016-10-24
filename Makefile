SHELL = bash

.PHONY: test test_verbose test_py coverage clean

test:
	python2 algorithms.py
	python3 algorithms.py
	pypy    algorithms.py

test_verbose:
	python2 algorithms.py -v
	python3 algorithms.py -v
	pypy    algorithms.py -v

test_py:
	python algorithms.py -v

coverage:
	python3 -mcoverage run algorithms.py
	python3 -mcoverage html

clean:
	rm -fr .coverage htmlcov/
	find -name '*.pyc' -delete
	find -name __pycache__ -delete
