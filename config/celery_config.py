from consumer.helper.validators import get_env_variable
from celery import Celery

app = Celery(
    'storage_file_microservices_s3_fastapi',
    backend=get_env_variable("BACKEND"),
    broker=get_env_variable("BROKER"),
)

app.autodiscover_tasks([
    'consumer.handler.files',
    'consumer.handler.catalog.create',
    'consumer.handler.catalog.collection',
    'consumer.handler.catalog.delete',
    'consumer.handler.files.upload',
    'consumer.handler.files.collection',
    'consumer.handler.files.collection_one',
    'endpoints.files.upload',
    'endpoints.files.delete'
], force=True)

# Konfiguracja Celery
app.conf.update(
    broker=get_env_variable("BROKER"),
    result_backend=get_env_variable("BACKEND"),
    result_expires=3600,
    imports=(
        'consumer.services.s3.collection', 'consumer.services.s3.create',
        'consumer.handler.catalog.create', 'consumer.handler.catalog.collection',
        'consumer.handler.catalog.collection_one', 'consumer.handler.catalog.delete',
        'consumer.handler.catalog.download', 'consumer.handler.files.upload',
        'endpoints.files.upload', 'consumer.handler.files.collection', 'endpoints.files.delete',
        'consumer.handler.files.collection_one'
    ),
    accept_content=['application/json', 'pickle'],
    result_serializer='pickle',
    task_serializer='pickle',
    broker_connection_retry_on_startup=True,
    task_default_retry_delay=10,
    task_max_retries=3,
    worker_prefetch_multiplier=2,
)
