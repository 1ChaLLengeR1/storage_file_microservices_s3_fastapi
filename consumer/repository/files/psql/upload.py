from fastapi import UploadFile
from config.celery_config import app
from consumer.data.response import ResponseData
from .helper import validate_file_extensions


@app.task(serializer="pickle")
def upload_file_psql(bucket_name: str, catalog_id: str, key_create: str, files: list[UploadFile]) -> ResponseData:
    try:

        invalid_files = validate_file_extensions(files)
        if not invalid_files['is_valid']:
            return ResponseData(
                is_valid=invalid_files['is_valid'],
                status=invalid_files['status'],
                status_code=invalid_files['status_code'],
                data=invalid_files['data']
            )

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data="poszło"
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
