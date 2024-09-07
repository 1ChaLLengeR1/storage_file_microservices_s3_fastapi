import pytest
from config.celery_config import app
from decouple import config
from consumer.handler.catalog.create import handler_create_catalog
from consumer.helper.random import createRandom

@app.task
def test_handler_create_catalog():

    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"

    response_data_catalog = handler_create_catalog(bucket_name, catalog_name, key_create)

    if response_data_catalog.error is not None:
        pytest.fail(f"Error from test handler create catalog: {response_data_catalog.error}")

    assert response_data_catalog.error is None, f"Error from test handler create catalog S3: {response_data_catalog.error}"

