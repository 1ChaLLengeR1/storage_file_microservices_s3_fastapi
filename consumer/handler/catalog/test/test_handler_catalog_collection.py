import pytest
from config.celery_config import app
from decouple import config
from consumer.handler.catalog.create import handler_create_catalog
from consumer.handler.catalog.collection import handler_collection_catalog
from consumer.handler.catalog.collection_one import handler_collection_one_catalog
from consumer.helper.random import createRandom
from consumer.data.error import ResponseError

@app.task
def test_handler_collection_catalog():
    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"
    handler_create_catalog(bucket_name, catalog_name, key_create)

    bucket_name = config("AWS_BUCKET_NAME")
    key_main = "test1"

    response_collection = handler_collection_catalog(bucket_name, key_main)

    if isinstance(response_collection, ResponseError):
        pytest.fail(f"Error from test handler collection catalog: {response_collection}")

    assert len(response_collection) > 0, "Folder tree is empty, expected some data."

    assert isinstance(response_collection, dict), "Expected folder_tree to be a dictionary."

    print("Test handler collection catalog passed!")


def test_handler_collection_one_catalog():
    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"
    response_create = handler_create_catalog(bucket_name, catalog_name, key_create)

    key_main = "test1"
    response_collection_one = handler_collection_one_catalog(response_create.id, key_main)

    if isinstance(response_collection_one, ResponseError):
        pytest.fail(f"Error from test handler collection one catalog: {response_collection_one}")

    assert isinstance(response_collection_one, dict), "Expected collection one to be a dictionary."

    assert response_create.name == response_collection_one['name'], (
        f"Expected name from response_create to match name from response_collection_one, "
        f"but got {response_create.name} and {response_collection_one['name']}"
    )

    print("Test handler collection one catalog passed!")