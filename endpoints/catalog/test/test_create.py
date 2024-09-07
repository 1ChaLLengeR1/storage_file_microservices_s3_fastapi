import pytest
from fastapi.testclient import TestClient
from consumer.helper.random import createRandom
from main import app
from decouple import config

client = TestClient(app)
def test_endpoint_post_create_catalog():

    data = {
        "bucket_name": config("AWS_BUCKET_NAME"),
        "catalog_name": createRandom("test", 10)
    }
    headers = {
        "key_create": "test"
    }
    url: str = "/catalog/create"

    response_create = client.post(url, headers=headers, json=data)
    response_data_create = response_create.json()
    assert response_create.status_code == 200
    assert isinstance(response_data_create["task_id"], str)

    response_task_id: str = response_data_create.get("task_id")
    url_task_status = f"/tasks/{response_task_id}"
    response_task_status = client.get(url_task_status)

    assert response_task_status.status_code == 200
    response_data = response_task_status.json()

    assert "status" in response_data
    assert response_data["status"] in ["Pending", "Success", "Failure"]
    assert "result" in response_data
    assert "error" in response_data["result"]
    assert response_data["result"]["error"] is None