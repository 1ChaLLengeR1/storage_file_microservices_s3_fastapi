migration_up:
	alembic upgrade head

migration_down:
	alembic downgrade base

migration_revision:
	alembic revision --autogenerate -m "new tables"

run_test:
	pytest -r w

