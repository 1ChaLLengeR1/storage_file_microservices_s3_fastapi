from celery import Celery

app = Celery(
    'storage_file_microservices_s3_fastapi',
    broker='pyamqp://guest@localhost//',
    backend='redis://localhost:6379/0'
)

