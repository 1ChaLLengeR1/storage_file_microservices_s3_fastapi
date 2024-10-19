import pytest
from decouple import config
from consumer.services.s3.create import create_catalog
from consumer.helper.random import createRandom
def test_create_catalog():

    bucket_name = config("AWS_BUCKET_NAME")
    catalog_name = createRandom("test", 20)

    response_data_catalog = create_catalog(bucket_name, catalog_name)

    if response_data_catalog.error is not None:
        pytest.fail(f"Error from test create catalog S3: {response_data_catalog.error}")

    assert response_data_catalog.error is None, f"Error from test create catalog S3: {response_data_catalog.error}"