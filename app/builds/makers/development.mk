.PHONY: clean format lint dev console dev_console

clean:
	pipenv clean
	pipenv --rm
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

format:
	pipenv run format

lint:
	pipenv run lint

dev:
	FLASK_ENV=development pipenv run dev

console:
	pipenv run console

dev_console:
	FLASK_ENV=development pipenv run console

all: clean install tests run
