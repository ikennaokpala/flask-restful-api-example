.PHONY: db db_init db_create db_drop db_migrate db_migration db_seed 

db: 
	pipenv run db_$(call args, init)

db_init:
	pipenv run db_init

db_create:
	pipenv run db_create

db_seed:
	pipenv run db_seed

db_drop:
	pipenv run db_drop

db_migration:
	pipenv run db_migration

db_migrate:
	pipenv run db_migrate
