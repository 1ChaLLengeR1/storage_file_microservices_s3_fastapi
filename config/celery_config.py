from celery import Celery

app = Celery(
    'storage_file_microservices_s3_fastapi',
    broker='pyamqp://guest@localhost//',
    backend='redis://localhost:6379/0'
)

app.conf.update(
    result_expires=120,
    imports=('consumer.services.s3.collection', 'consumer.services.s3.create', 'consumer.handler.catalog.create'),
    accept_content = ['application/json', 'json', 'pickle'],
    result_serializer='pickle',
    task_serializer='pickle'
)