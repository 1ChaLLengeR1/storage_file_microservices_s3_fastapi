migration_up:
	alembic downgrade base

migration_down:
	alembic upgrade head