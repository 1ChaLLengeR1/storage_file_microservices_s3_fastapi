from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.repository.files.psql.delete import delete_files_psql
from consumer.helper.validators import is_valid_uuid


@app.task(serializer='pickle')
def handler_delete_files(bucket_name: str, list_id: list[str], key_delete: str) -> ResponseData:
    try:

        for idx, file_id in enumerate(list_id):
            if not is_valid_uuid(file_id):
                return ResponseData(
                    is_valid=False,
                    status="ERROR",
                    data={"error": f"Invalid UUID format at index {idx}: {file_id}"},
                    status_code=400
                )

        response_collection = delete_files_psql(bucket_name, list_id, key_delete)
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
