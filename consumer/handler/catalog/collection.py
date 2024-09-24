from database.database import get_db
from database.modals.Catalog.models import Catalog
from pydantic import BaseModel
from config.celery_config import app


@app.task(serializer="pickle")
def handler_collection_catalog():

    db_gen = get_db()
    db = next(db_gen)

    data = [
        {"id": "997a01b0-7f63-44be-a19a-d8523a7e3652", "bucketName": "storage-fastapi-s3", "name": "test1",
         "originalName": "test1_2PJoc22YNh", "path": "test1/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test1%2F"},
        {"id": "b57e2c0c-548b-4f33-9eba-631024749512", "bucketName": "storage-fastapi-s3", "name": "test2",
         "originalName": "test2_jFLntw0MvQ", "path": "test2/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2F"},
        {"id": "b274ae2f-090e-4d39-899f-8df4926c3eba", "bucketName": "storage-fastapi-s3", "name": "test3",
         "originalName": "test3_NKQOt3kVD6", "path": "test2/test3/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest3%2F"},
        {"id": "b274ae2f-090e-4d39-899f-8df4926c3eba", "bucketName": "storage-fastapi-s3", "name": "test3",
         "originalName": "test3_NKQOt3kVD6", "path": "test2/test3/test4/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest3%2F"},
        {"id": "b274ae2f-090e-4d39-899f-8df4926c3eba", "bucketName": "storage-fastapi-s3", "name": "test3",
         "originalName": "test3_NKQOt3kVD6", "path": "test2/test3/test4/test5/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest3%2F"},
        {"id": "b274ae2f-090e-4d39-899f-8df4926c3eba", "bucketName": "storage-fastapi-s3", "name": "test3",
         "originalName": "test3_NKQOt3kVD6", "path": "test2/test3/test4/test5/test6/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest3%2F"},
        {"id": "d20cde85-f770-4488-a063-e336aed95507", "bucketName": "storage-fastapi-s3", "name": "test4",
         "originalName": "test4_VR2XpkdXgo", "path": "test2/test4/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest4%2F"},
        {"id": "3d61b363-6b6c-4dbb-894a-8f51b1bacfa9", "bucketName": "storage-fastapi-s3", "name": "test5",
         "originalName": "test5_8kWjkHOsvr", "path": "test2/test5/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest5%2F"},
        {"id": "50cc375a-b352-4d0b-85ce-9eb7ed5bc469", "bucketName": "storage-fastapi-s3", "name": "test4",
         "originalName": "test4_FiHgSKuq03", "path": "test2/test4/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest4%2F"},
        {"id": "8a32f780-4dcb-410b-a85d-769b00c695af", "bucketName": "storage-fastapi-s3", "name": "test6",
         "originalName": "test6_W5avjgoji2", "path": "test2/test5/test6/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest5%2Ftest6%2F"},
        {"id": "bb5c5364-3037-4e48-a3a3-9d9941e747f5", "bucketName": "storage-fastapi-s3", "name": "test7",
         "originalName": "test7_M5Q1sm1rJg", "path": "test2/test5/test7/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest5%2Ftest7%2F"},
        {"id": "797bd711-da96-491c-9212-222c2aab3fda", "bucketName": "storage-fastapi-s3", "name": "test8",
         "originalName": "test8_vog5N1i1zO", "path": "test2/test5/test7/test8/",
         "url": "https://storage-fastapi-s3.s3.amazonaws.com/test2%2Ftest5%2Ftest7%2Ftest8%2F"},
    ]

    folder_tree = {}

    for entry in data:
        folder_path = entry["path"]
        parts = folder_path.strip("/").split("/")
        current_node = folder_tree

        print(parts)

        # Przechodzimy przez wszystkie foldery w ścieżce
        for part in parts[:-1]:
            # print(part)
            if part not in current_node:
                current_node[part] = {
                    "subfolders": {}
                }
            current_node = current_node[part]["subfolders"]

        # Dodaj dane katalogu na tym samym poziomie co subfolders
        folder_name = parts[-1]  # Nazwa folderu
        current_node[folder_name] = {
            "id": entry["id"],
            "bucketName": entry["bucketName"],
            "name": entry["name"],
            "originalName": entry["originalName"],
            "path": entry["path"],
            "url": entry["url"],
            "subfolders": {}
        }

    return folder_tree
