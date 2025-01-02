import pytest
from decouple import config
from consumer.repository.catalog.psql.delete import delete_catalog_psql
from consumer.repository.catalog.psql.collection_one import collection_one_catalog_psql
from consumer.repository.catalog.psql.create import create_catalog_psql
from consumer.helper.random import createRandom


def test_delete_catalog_psql():
    catalog_name = createRandom("test")
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"
    response_create = create_catalog_psql(bucket_name, catalog_name, key_create)

    key_main = "test1"
    response_collection_one = collection_one_catalog_psql(response_create['data'][0]['id'], key_main)
    if not response_collection_one['is_valid']:
        pytest.fail(f"Error from test collection_catalog_psql: {response_collection_one['data']}")

    response_delete = delete_catalog_psql(response_create['data'][0]['id'], bucket_name, key_main)
    if not response_delete['is_valid']:
        pytest.fail(f"Error from test delete_catalog_psql: {response_delete['data']}")

    assert isinstance(response_delete['data'], list), "Expected 'data' to be a list."
    assert isinstance(response_delete['data'][0], dict), "Expected the first item in 'data' to be a dictionary."

    print("Test delete_catalog_psql passed!")
