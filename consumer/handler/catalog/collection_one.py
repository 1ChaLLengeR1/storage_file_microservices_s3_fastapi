from config.redis_client import get_cache_data, set_cache_data
from config.celery_config import app
from consumer.repository.catalog.psql.collection_one import collection_one_catalog_psql
from consumer.data.response import ResponseData


@app.task(serializer="pickle")
def handler_collection_one_catalog(catalog_id: str, key_main: str):
    try:
        cache_key = f"catalog_{catalog_id}"
        cached_data = get_cache_data(cache_key)
        if cached_data:
            return cached_data

        response_collection_one = collection_one_catalog_psql(catalog_id, key_main)
        if not response_collection_one['is_valid']:
            return ResponseData(
                is_valid=response_collection_one['is_valid'],
                status=response_collection_one['status'],
                status_code=response_collection_one['status_code'],
                data=response_collection_one['data']
            )

        set_cache_data(cache_key, response_collection_one)
        return ResponseData(
            is_valid=response_collection_one['is_valid'],
            status=response_collection_one['status'],
            status_code=response_collection_one['status_code'],
            data=response_collection_one['data']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )