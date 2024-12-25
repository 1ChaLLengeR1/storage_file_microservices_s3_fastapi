from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.helper.validators import is_valid_uuid
from consumer.repository.files.psql.collection import collection_files_psql


@app.task(serializer='pickle')
def handler_collection_files(catalog_id: str, key_main: str) -> ResponseData:
    try:

        check_uuid = is_valid_uuid(catalog_id)
        if not check_uuid:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data="invalid uuid format",
                status_code=400
            )

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
            status_code=500,
            data={"error": str(e)}
        )
