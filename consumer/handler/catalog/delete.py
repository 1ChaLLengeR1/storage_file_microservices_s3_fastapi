from config.celery_config import app
from config.redis_client import delete_cache_by_prefix
from consumer.repository.catalog.psql.delete import delete_catalog_psql
from consumer.data.response import ResponseData


@app.task(serializer="pickle")
def handler_delete_catalog(catalog_id: str, bucket_name: str, key_main: str):
    try:
        response_delete = delete_catalog_psql(catalog_id, bucket_name, key_main)
        if not response_delete['is_valid']:
            return ResponseData(
                is_valid=response_delete['is_valid'],
                status=response_delete['status'],
                status_code=response_delete['status_code'],
                data=response_delete['data']
            )

        delete_cache_by_prefix("catalog_")
        return ResponseData(
            is_valid=response_delete['is_valid'],
            status=response_delete['status'],
            status_code=response_delete['status_code'],
            data=response_delete['data']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
