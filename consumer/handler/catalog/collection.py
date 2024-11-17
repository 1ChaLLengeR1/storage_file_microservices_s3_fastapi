from config.redis_client import get_cache_data, set_cache_data
from config.celery_config import app
from consumer.repository.catalog.psql.collection import collection_catalog_psql
from consumer.data.response import ResponseData


@app.task(serializer="pickle")
def handler_collection_catalog(name_bucket: str, key_main: str) -> ResponseData:
    try:

        cache_key = f"catalog_{name_bucket}"
        cached_data = get_cache_data(cache_key)
        if cached_data:
            print(cached_data)
            return cached_data

        response_collection = collection_catalog_psql(name_bucket, key_main)
        if not response_collection['is_valid']:
            return ResponseData(
                is_valid=response_collection['is_valid'],
                status=response_collection['status'],
                status_code=response_collection['status_code'],
                data=response_collection['data']
            )
        set_cache_data(cache_key, response_collection)
        return ResponseData(
            is_valid=response_collection['is_valid'],
            status=response_collection['status'],
            status_code=response_collection['status_code'],
            data=response_collection['data']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
