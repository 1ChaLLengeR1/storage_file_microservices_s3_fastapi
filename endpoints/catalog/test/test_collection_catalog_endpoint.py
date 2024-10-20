import pytest
from fastapi.testclient import TestClient
from consumer.helper.random import createRandom
from main import app
from decouple import config

client = TestClient(app)


def test_endpoint_post_collection_catalog():
    data = {
        "bucket_name": config("AWS_BUCKET_NAME"),
        "catalog_name": createRandom("test", 10)
    }
    headers = {
        "key_create": "test"
    }
    url: str = "/catalog/create"
    client.post(url, headers=headers, json=data)

    headers = {
        "key_main": "test1"
    }
    url_collection: str = "/collection/catalogs/storage-fastapi-s3"

    response_collection = client.get(url_collection, headers=headers)
    response_data_create = response_collection.json()
    assert response_collection.status_code == 200
    assert isinstance(response_data_create["task_id"], str)

    response_task_id: str = response_data_create.get("task_id")
    url_task_status = f"/tasks/{response_task_id}"
    response_task_status = client.get(url_task_status)

    assert response_task_status.status_code == 200
    response_data = response_task_status.json()
    assert "status" in response_data
    assert response_data["status"] in ["PENDING", "ERROR", "SUCCESS", "FAILURE"]
    if response_data["status"] == "ERROR":
        assert "error" in response_data["result"]
