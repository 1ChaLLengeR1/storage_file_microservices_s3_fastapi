import eventlet
eventlet.monkey_patch()

from celery import Celery

app = Celery(
    'storage_file_microservices_s3_fastapi',
    broker='pyamqp://guest@localhost//', #za pomocą lokalnie
    backend='redis://localhost:6379/0' #za pomocą lokalnie
    # broker='pyamqp://guest@rabbitmq_backend_microservice//',
    # backend='redis://redis_backend_microservice:6379/0'
)

app.conf.update(
    result_expires=120,
    imports=('consumer.services.s3.collection', 'consumer.services.s3.create', 'consumer.handler.catalog.create',
             'consumer.handler.catalog.collection', 'consumer.handler.catalog.collection_one'),
    accept_content=['application/json', 'json', 'pickle'],
    result_serializer='pickle',
    broker_connection_retry_on_startup=True,
    task_serializer='pickle'
)
