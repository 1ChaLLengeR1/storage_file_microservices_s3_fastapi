from fastapi import UploadFile
from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.repository.files.psql.upload import upload_file_psql


@app.task(serializer="pickle")
def handler_upload_file(bucket_name: str, catalog_id: str, key_create: str, files: list[UploadFile]) -> ResponseData:
    try:
        response_upload = upload_file_psql(bucket_name, catalog_id, key_create, files)
        if not response_upload['is_valid']:
            return ResponseData(
                is_valid=response_upload['is_valid'],
                status=response_upload['status'],
                status_code=response_upload['status_code'],
                data=response_upload['data']
            )

        return ResponseData(
            is_valid=response_upload['is_valid'],
            status=response_upload['status'],
            status_code=response_upload['status_code'],
            data=response_upload['data']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
