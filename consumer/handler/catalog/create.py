from config.celery_config import app
from config.redis_client import delete_cache_by_prefix
from consumer.repository.catalog.psql.create import create_catalog_psql
from consumer.data.response import ResponseData


@app.task(serializer="pickle")
def handler_create_catalog(bucket_name: str, name_catalog: str, key_create: str) -> ResponseData:
    try:
        response_catalog = create_catalog_psql(bucket_name, name_catalog, key_create)
        if not response_catalog['is_valid']:
            return ResponseData(
                is_valid=response_catalog['is_valid'],
                status_code=response_catalog['status_code'],
                status=response_catalog['status'],
                data=response_catalog['data']
            )

        delete_cache_by_prefix("collection_catalog_")
        return ResponseData(
            is_valid=response_catalog['is_valid'],
            status_code=response_catalog['status_code'],
            status=response_catalog['status'],
            data=response_catalog['data']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status_code=417,
            status="ERROR",
            data=str(e)
        )
