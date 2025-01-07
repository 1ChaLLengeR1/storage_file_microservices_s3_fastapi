import pytest
from decouple import config
from consumer.repository.files.psql.upload import upload_file_psql
from consumer.repository.files.psql.delete import delete_files_psql
from consumer.repository.catalog.psql.create import create_catalog_psql
from consumer.helper.random import createRandom
from config.config_app import IMG1, IMG2, IMG3, IMG4


def test_delete_files_psql():
    bucket_name = config("AWS_BUCKET_NAME")
    key_create = "test"
    key_delete = "test"
    files = [IMG1, IMG2, IMG3, IMG4]
    catalog_name = createRandom("test")

    response_create = create_catalog_psql(bucket_name, catalog_name, key_create)
    if not response_create['is_valid']:
        pytest.fail(f"Error from test create_catalog_psql: {response_create['data']}")

    response_upload = upload_file_psql(bucket_name, response_create['data'][0]['id'], key_create, files, False)
    if not response_upload['is_valid']:
        pytest.fail(f"Error from test upload_file_psql: {response_upload['data']}")

    assert len(response_upload['data']) > 0, "collection upload file is 0, expected some data."

    remove_list_id = [response_upload['data'][0]['id'], response_upload['data'][1]['id'],
                      response_upload['data'][2]['id']]

    response_delete = delete_files_psql(bucket_name, remove_list_id, key_delete)
    if not response_delete['is_valid']:
        pytest.fail(f"Error from test delete_files_psql: {response_delete['data']}")

    assert len(response_delete['data']) == 3, "delete files is 0, expected some data == 3."
