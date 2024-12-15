import eventlet

eventlet.monkey_patch(thread=False)

from consumer.helper.validators import get_env_variable
from celery import Celery
import logging

logger = logging.getLogger('celery')
logger.setLevel(logging.DEBUG)

app = Celery(
    'storage_file_microservices_s3_fastapi',
    broker=get_env_variable("BROKER"),
    backend=get_env_variable("BACKEND")
)

from config.test.test_redis_rabbitmq import test_rabbitmq

app.conf.update(
    result_expires=120,
    imports=(
        'consumer.services.s3.collection', 'consumer.services.s3.create',
        'consumer.handler.catalog.create',
        'consumer.handler.catalog.collection', 'consumer.handler.catalog.collection_one',
        'consumer.handler.catalog.delete', 'consumer.handler.catalog.download'),
    accept_content=['application/json', 'json', 'pickle'],
    result_serializer='pickle',
    result_backend=get_env_variable("BACKEND"),
    broker_connection_retry_on_startup=True,
    task_serializer='pickle',
    task_track_started=True,
    worker_log_format='[%(asctime)s: %(levelname)s] %(message)s',
    worker_task_log_format='[%(asctime)s: %(levelname)s] %(task_name)s - %(message)s',
)



