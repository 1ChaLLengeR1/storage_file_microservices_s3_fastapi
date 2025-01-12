import pytest
import time
from decouple import config
from config.config_app import IMG1
from consumer.helper.random import createRandom
from consumer.repository.catalog.psql.create import create_catalog_psql
from consumer.repository.files.psql.upload import upload_file_psql
from consumer.repository.files.psql.download import download_file_psql
from consumer.helper.files import check_catalog_is_empty, clear_folders_and_zips
from config.config_app import DOWNLOAD_FOLDER


def test_download_file_psql():
    catalog_name = createRandom("test")
    key_main = "test1"
    key_create = "test"
    bucket_name = config("AWS_BUCKET_NAME")
    files = [IMG1]

    response_create = create_catalog_psql(bucket_name, catalog_name, key_create)
    if not response_create['is_valid']:
        pytest.fail(f"Error from test create_catalog_psql: {response_create['data']}")

    response_upload = upload_file_psql(bucket_name, response_create['data'][0]['id'], key_create, files, False)
    if not response_upload['is_valid']:
        pytest.fail(f"Error from test upload_file_psql: {response_upload['data']}")

    assert len(response_upload['data']) > 0, "collection upload file is 0, expected some data."

    response_download = download_file_psql(response_upload['data'][0]['id'], bucket_name, key_main)
    if not response_download['is_valid']:
        pytest.fail(f"Error from test download_file_psql: {response_download['data']}")

    assert isinstance(response_download['data'], dict), "Expected json."

    time.sleep(4)

    check_catalog = check_catalog_is_empty(DOWNLOAD_FOLDER)
    if check_catalog:
        pytest.fail(f"Catalog download is empty after download from s3")

    clear_folders_and_zips(DOWNLOAD_FOLDER, True)
