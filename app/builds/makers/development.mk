.PHONY: clean format lint server console all

clean:
	pipenv clean
	pipenv --rm
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

format:
	pipenv run format

lint:
	pipenv run lint

server:
	FLASK_ENV=development pipenv run server

console:
	@if [[ $(call args, prod) == "dev" ]] ; then \
		FLASK_ENV=development pipenv run console; \
	else \
		FLASK_ENV=production pipenv run console; \
	fi

all: clean install tests server
