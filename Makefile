SHELL := /bin/bash -eu -o pipefail

pylint:
	pylint src tests

mypy:
	mypy src

flake8:
	flake8 src tests

pytest:
	PYTHONPATH=src coverage run -m pytest

coverage: pytest
	coverage report

wheel: clean
	python -m build . --wheel

clean:
	rm -rvf ./build/ ./dist/ .coverage ./src/custolint.egg-info/ README.html ./.mypy_cache/
	rm -rvf	./.pytest_cache/ ./tests/.pytest_cache/ ./htmlcov/
	#$(MAKE) --directory=docs clean_docs

deploy_to_pypy: wheel # validate
	twine upload dist/*

validate: coverage mypy pylint flake8
