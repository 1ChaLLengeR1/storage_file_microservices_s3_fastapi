from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.repository.files.psql.upload import upload_file_psql
from consumer.helper.validators import is_valid_uuid
from consumer.repository.files.psql.helper import validate_file_extensions


@app.task(serializer='pickle')
def handler_upload_file(bucket_name: str, catalog_id: str, key_create: str, files: list[str]) -> ResponseData:
    try:

        check_uuid = is_valid_uuid(catalog_id)
        if not check_uuid:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data="invalid uuid format",
                status_code=400
            )

        if len(files) == 0:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                status_code=400,
                data={"error": "No photo added!"}
            )

        invalid_files = validate_file_extensions(files)
        if not invalid_files['is_valid']:
            return ResponseData(
                is_valid=invalid_files['is_valid'],
                status=invalid_files['status'],
                status_code=invalid_files['status_code'],
                data=invalid_files['data']
            )

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
            status_code=500,
            data={"error": str(e)}
        )
