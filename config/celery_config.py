from celery import Celery

app = Celery(
    'storage_file_microservices_s3_fastapi',
    broker='pyamqp://guest@localhost//',
    backend='redis://localhost:6379/0'
)

app.conf.result_expires = 120
app.conf.imports = ('consumer.services.s3.collection', "consumer.services.s3.create")
