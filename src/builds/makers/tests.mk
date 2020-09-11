.PHONY: tests test

tests:
	FLASK_ENV=test pipenv run db_create
	FLASK_ENV=test pipenv run tests
	FLASK_ENV=test pipenv run db_drop

test:
	FLASK_ENV=test pipenv run db_create
	FLASK_ENV=test pipenv run test $(call args, src/tests/test*.py)
	FLASK_ENV=test pipenv run db_drop
