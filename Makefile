check: flake8 test

tidy:
	black -l 79 agents

flake8:
	black --check -l 79 agents

test:
	python -m unittest discover -s tests

install:
	pip install .[dev]

sdist:
	python setup.py sdist

clean:
	rm -rf dist/

livedocs:
	sphinx-autobuild docs/source docs/build/html

builddocs:
	cd docs && make html
