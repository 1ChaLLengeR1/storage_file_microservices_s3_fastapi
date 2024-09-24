from config.celery_config import app
from consumer.services.s3.collection import collection_one

@app.task(serializer="pickle")
def handler_collection_one_files(bucket_name: str, name_file: str):
    response_file = collection_one(bucket_name, name_file)
    return response_file

