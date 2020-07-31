sdist:
	python setup.py sdist

clean:
	rm -rf dist/

check:
	flake8
