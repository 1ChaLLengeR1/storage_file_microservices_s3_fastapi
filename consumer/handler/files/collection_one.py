from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.helper.validators import is_valid_uuid
from consumer.repository.files.psql.collection_one import collection_one_file_psql


@app.task(serializer="pickle")
def handler_collection_one_file(file_id: str, key_main: str) -> ResponseData:
    try:
        check_uuid = is_valid_uuid(file_id)
        if not check_uuid:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data="invalid uuid format",
                status_code=400
            )

        response_collection_one = collection_one_file_psql(file_id, key_main)
        if not response_collection_one['is_valid']:
            return ResponseData(
                is_valid=response_collection_one['is_valid'],
                status=response_collection_one['status'],
                data=response_collection_one['data'],
                status_code=response_collection_one['status_code']
            )
        return ResponseData(
            is_valid=response_collection_one['is_valid'],
            status=response_collection_one['status'],
            data=response_collection_one['data'],
            status_code=response_collection_one['status_code']
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=500,
            data={"error": str(e)}
        )
