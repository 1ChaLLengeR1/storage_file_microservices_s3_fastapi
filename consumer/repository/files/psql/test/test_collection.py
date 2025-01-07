import pytest
from decouple import config
from consumer.repository.files.psql.upload import upload_file_psql
from consumer.repository.files.psql.collection import collection_files_psql
from consumer.repository.files.psql.collection_one import collection_one_file_psql
from consumer.repository.catalog.psql.create import create_catalog_psql
from consumer.helper.random import createRandom
from config.config_app import IMG1, IMG2, IMG3, IMG4


def test_collection_files_psql():
    bucket_name = config("AWS_BUCKET_NAME")
    key_main = "test1"
    key_create = "test"
    files = [IMG1, IMG2, IMG3, IMG4]
    catalog_name = createRandom("test")

    response_create = create_catalog_psql(bucket_name, catalog_name, key_create)
    if not response_create['is_valid']:
        pytest.fail(f"Error from test create_catalog_psql: {response_create['data']}")

    response_upload = upload_file_psql(bucket_name, response_create['data'][0]['id'], key_create, files, False)
    if not response_upload['is_valid']:
        pytest.fail(f"Error from test upload_file_psql: {response_upload['data']}")

    assert len(response_upload['data']) > 0, "collection upload file is 0, expected some data."

    response_collection_files = collection_files_psql(response_create['data'][0]['id'], key_main)
    if not response_collection_files['is_valid']:
        pytest.fail(f"Error from test collection_files_psql: {response_collection_files['data']}")

    assert len(response_collection_files['data']) > 0, "collection files is 0, expected some data."


def test_collection_one_file_psql():
    bucket_name = config("AWS_BUCKET_NAME")
    key_main = "test1"
    key_create = "test"
    files = [IMG1]
    catalog_name = createRandom("test")

    response_create = create_catalog_psql(bucket_name, catalog_name, key_create)
    if not response_create['is_valid']:
        pytest.fail(f"Error from test create_catalog_psql: {response_create['data']}")

    response_upload = upload_file_psql(bucket_name, response_create['data'][0]['id'], key_create, files, False)
    if not response_upload['is_valid']:
        pytest.fail(f"Error from test upload_file_psql: {response_upload['data']}")

    response_collection_one_file = collection_one_file_psql(response_upload['data'][0]['id'], key_main)
    if not response_collection_one_file['is_valid']:
        pytest.fail(f"Error from test collection_one_file_psql: {response_collection_one_file['data']}")

    assert isinstance(response_collection_one_file['data'], dict), "Expected json."
