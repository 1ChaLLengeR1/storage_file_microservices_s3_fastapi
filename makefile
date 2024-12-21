migration_up:
	alembic upgrade head

migration_down:
	alembic downgrade base

migration_revision:
	alembic revision --autogenerate -m "new tables"

run_test:
	pytest -r w

run_worker:
	celery -A config.celery_config.app worker --concurrency=4 -P eventlet --loglevel=info

run_flower:
	celery -A config.celery_config.app flower --basic_auth=admin:admin

run_worker_status:
	celery -A config.celery_config.app status

run_app:
	uvicorn main:app --reload --log-level debug --port 7000