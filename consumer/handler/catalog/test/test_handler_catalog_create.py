import pytest
from config.celery_config import app
from decouple import config
from consumer.handler.catalog.create import handler_create_catalog
from consumer.helper.random import createRandom
from consumer.handler.catalog.data.create import HandlerCatalogResponse

@app.task
def test_handler_create_catalog():

    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"

    response_data_catalog = handler_create_catalog(bucket_name, catalog_name, key_create)

    # if isinstance(response_data_catalog, ResponseError):
    #     pytest.fail(f"Error from test handler create catalog: {response_data_catalog}")

    assert isinstance(response_data_catalog,
                      HandlerCatalogResponse), "Expected HandlerCatalogResponse but got something else."
    assert response_data_catalog.name is not None, "Catalog name should not be None"

