import pytest
from config.celery_config import app
from decouple import config
from consumer.repository.catalog.psql.collection import collection_catalog_psql
from consumer.repository.catalog.psql.collection_one import collection_one_catalog_psql
from consumer.repository.catalog.psql.create import create_catalog_psql
from consumer.helper.random import createRandom


@app.task
def test_collection_catalog_psql():
    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"
    create_catalog_psql(bucket_name, catalog_name, key_create)

    bucket_name = config("AWS_BUCKET_NAME")
    key_main = "test1"

    response_collection = collection_catalog_psql(bucket_name, key_main)
    if not response_collection['is_valid']:
        pytest.fail(f"Error from test collection_catalog_psql: {response_collection['data']}")

    assert len(response_collection['data']) > 0, "Folder tree is empty, expected some data."
    assert isinstance(response_collection['data'], dict), "Expected folder_tree to be a dictionary."

    print("Test collection_catalog_psql passed!")

@app.task
def test_collection_one_catalog_psql():
    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"
    response_create = create_catalog_psql(bucket_name, catalog_name, key_create)

    key_main = "test1"
    response_collection_one = collection_one_catalog_psql(response_create['data'][0]['id'], key_main)
    if not response_collection_one['is_valid']:
        pytest.fail(f"Error from test collection_catalog_psql: {response_collection_one['data']}")

    assert isinstance(response_collection_one['data'], dict), "Expected collection one to be a dictionary."

    assert response_create['data'][0]['name'] == response_collection_one['data']['name'], (
        f"Expected name from response_create to match name from response_collection_one, "
        f"but got {response_create['data']['name']} and {response_collection_one['data']['name']}"
    )

    print("Test collection_one_catalog_psql passed!")
