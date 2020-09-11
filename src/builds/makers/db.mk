.PHONY: db db_branches db_create db_current db_downgrade db_drop db_edit db_heads db_history db_init db_merge db_migrate db_migration db_revision db_seed db_show db_stamp

db: 
	pipenv run db_$(call args, init)

db_branches:
	pipenv run db_branches

db_create:
	pipenv run db_create

db_current:
	pipenv run db_current

db_downgrade:
	pipenv run db_downgrade

db_drop:
	pipenv run db_drop

db_edit:
	pipenv run db_edit

db_heads:
	pipenv run db_heads

db_history:
	pipenv run db_history

db_init:
	pipenv run db_init

db_merge:
	pipenv run db_merge

db_migration:
	pipenv run db_migration

db_migrate:
	pipenv run db_migrate

db_revision:
	pipenv run db_revision

db_seed:
	pipenv run db_seed

db_show:
	pipenv run db_show

db_stamp:
	pipenv run db_stamp
