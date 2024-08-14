from config.celery_config import app

@app.task
def test_rabbitmq():
    return 'RabbitMQ work!'

def test_rabbitmq_connection():
    try:
        result = test_rabbitmq.delay()
        return True, result
    except Exception as e:
        return False, str(e)

def test_redis_connection():
    try:
        result = test_rabbitmq.delay()
        result_value = result.get(timeout=10)
        return True, result_value
    except Exception as e:
        return False, str(e)
