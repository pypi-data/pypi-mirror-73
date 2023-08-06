all: install_dev_dependencies install test lint test_release_setup

install_dev_dependencies:
	pip install -r dev_requirements.txt

install: clean
	python setup.py install

clean:
	rm -f .coverage
	rm -f coverage.xml
	rm -Rf .eggs
	rm -Rf .pytest_cache
	rm -Rf __pycache__
	rm -Rf **/__pycache__/*
	rm -Rf **/*.c
	rm -Rf **/*.so
	rm -Rf **/*.pyc
	rm -Rf dist/
	rm -Rf build/
	rm -Rf docs/build
	rm -Rf import_git_files.egg-info

test:
	coverage run --source=import_git_files -m pytest -vvv tests/
	coverage report -m
	coverage xml

lint:
	python -m pylint import_git_files

test_release_setup:
	twine check dist/*
