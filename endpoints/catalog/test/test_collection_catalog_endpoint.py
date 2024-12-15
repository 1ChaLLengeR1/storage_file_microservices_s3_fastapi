import pytest
from fastapi.testclient import TestClient
from consumer.helper.random import createRandom
from main import app
from config.celery_config import app as celery_app
from decouple import config

client = TestClient(app)


@celery_app.task
def test_endpoint_collection_catalog():
    url_collection: str = "/collection/catalogs/storage-fastapi-s3"

    headers = {
        "key_main": "test1"
    }

    response_collection = client.get(url_collection, headers=headers)

    print(response_collection.json())
    assert response_collection.status_code == 200

# def test_endpoint_collection_one_catalog():
#     data_create = {
#         "bucket_name": config("AWS_BUCKET_NAME"),
#         "catalog_name": createRandom("test", 10)
#     }
#     headers_create = {
#         "key_create": "test"
#     }
#     url_create: str = "/catalog/create"
#     response_create = client.post(url_create, headers=headers_create, json=data_create)
#     response_data_create = response_create.json()
#     assert response_create.status_code == 200
#     assert isinstance(response_data_create["task_id"], str)
#
#     response_task_id: str = response_data_create.get("task_id")
#     url_task_status = f"/tasks/{response_task_id}"
#     response_task_data_create = client.get(url_task_status)  # dane z create
#     response_data_json_create = response_task_data_create.json()
#
#     headers_collection_one = {
#         "key_main": "test1"
#     }
#     url_collection_one: str = f"/collection/catalog/{response_data_json_create['result']['id']}"
#     response_collection_one = client.get(url_collection_one, headers=headers_collection_one)
#     response_data_collection_one = response_collection_one.json()
#     assert response_collection_one.status_code == 200
#     assert isinstance(response_data_collection_one["task_id"], str)
#
#     response_task_collection_one_id: str = response_data_collection_one.get("task_id")
#     url_task_collection_one_status = f"/tasks/{response_task_collection_one_id}"  # dane z collection one
#     response_data_collection_one = client.get(url_task_collection_one_status)
#     response_data_json_collection_one = response_data_collection_one.json()
#
#     assert response_data_json_create['result']['name'] == response_data_json_collection_one['result']['name'], (
#         f"Expected name from response_create to match name from response_collection_one, "
#         f"but got {response_data_json_create['result']['name']} and {response_data_json_collection_one['result']['name']}"
#     )
