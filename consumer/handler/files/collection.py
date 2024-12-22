from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.repository.files.psql.collection import collection_files_psql


@app.task(serializer='pickle')
def handler_collection_files(catalog_id: str, key_main: str) -> ResponseData:
    try:
        response_collection = collection_files_psql(catalog_id, key_main)
        if not response_collection['is_valid']:
            return ResponseData(
                is_valid=response_collection['is_valid'],
                status=response_collection['status'],
                data=response_collection['data'],
                status_code=response_collection['status_code']
            )
        return ResponseData(
            is_valid=response_collection['is_valid'],
            status=response_collection['status'],
            data=response_collection['data'],
            status_code=response_collection['status_code']
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
