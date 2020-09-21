sdist:
	python setup.py sdist

clean:
	rm -rf dist/

check: flake8 test

tidy:
	black -l 79 agents

flake8:
	flake8

test:
	python -m unittest discover -s tests
