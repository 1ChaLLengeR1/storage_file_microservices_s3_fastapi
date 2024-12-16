from config.celery_config import app
from consumer.data.response import ResponseData
import redis
from celery.result import AsyncResult


@app.task(name='config.test.test_redis_rabbitmq.test_rabbitmq')
def test_rabbitmq():
    return ResponseData(
        is_valid=True,
        status="SUCCESS",
        data="RabbitMQ work!",
        status_code=200
    )


def test_rabbitmq_connection():
    try:

        result = test_rabbitmq.delay()

        if result.successful():
            return True, result.result
        else:
            return False, "Task failed"

    except Exception as e:
        return False, str(e)


def test_redis_connection():
    try:

        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if r.ping():
            return True, "Redis connection successful"
        else:
            return False, "Redis connection failed"
    except Exception as e:
        return False, str(e)
