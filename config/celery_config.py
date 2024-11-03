from consumer.helper.validators import get_env_variable
from celery import Celery


app = Celery(
    'storage_file_microservices_s3_fastapi',
    broker=get_env_variable("BROKER"),
    backend=get_env_variable("BACKEND")
)

app.conf.update(
    result_expires=120,
    imports=('consumer.services.s3.collection', 'consumer.services.s3.create', 'consumer.handler.catalog.create',
             'consumer.handler.catalog.collection', 'consumer.handler.catalog.collection_one',
             'consumer.handler.catalog.delete', 'consumer.handler.catalog.download'),
    accept_content=['application/json', 'json', 'pickle'],
    result_serializer='pickle',
    broker_connection_retry_on_startup=True,
    task_serializer='pickle'
)
