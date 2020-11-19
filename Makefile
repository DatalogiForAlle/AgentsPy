sdist:
	python setup.py sdist

clean:
	rm -rf dist/

check: flake8 test

tidy:
	black -l 79 agents

flake8:
	flake8 --exclude=blockly

test:
	python -m unittest discover -s tests

livedocs:
	sphinx-autobuild docs/source docs/build/html

builddocs:
	cd docs && make html
