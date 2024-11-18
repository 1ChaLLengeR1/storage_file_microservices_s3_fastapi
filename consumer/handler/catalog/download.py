from config.celery_config import app
from consumer.data.response import ResponseData
from consumer.helper.files import clear_folders_and_zips
from consumer.repository.catalog.psql.download import download_catalog_psql


@app.task(serializer="pickle")
def handler_download_catalog(catalog_id: str, bucket_name: str, key_main: str) -> ResponseData:
    try:
        response_download = download_catalog_psql(catalog_id, bucket_name, key_main)
        if not response_download['is_valid']:
            return ResponseData(
                is_valid=response_download['is_valid'],
                status=response_download['status'],
                status_code=response_download['status_code'],
                data=response_download['data']
            )

        clean_up_task.apply_async(args=[response_download['data']['path_remove']], countdown=5)
        return ResponseData(
            is_valid=response_download['is_valid'],
            status=response_download['status'],
            status_code=response_download['status_code'],
            data=response_download['data']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )


@app.task(serializer="pickle")
def clean_up_task(directory):
    clear_folders_and_zips(directory)
