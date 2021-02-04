check: flake8 test

tidy:
	black -l 79 agents

flake8:
	black --check --exclude=blockly -l 79 agents

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


publish_new_release:
	@echo -n "Are you sure you want to publish a new release? [y/N] " && read ans && [ $${ans:-N} = y ]
	rm -rf dist/
	python3 -m pip install --upgrade build
	python3 -m build
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository pypi dist/*
