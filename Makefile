install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 kas

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install .

test-cov:
	poetry run pytest --cov=kas
