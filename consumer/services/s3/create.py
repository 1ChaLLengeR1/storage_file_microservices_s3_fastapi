from config.celery_config import app
from config.s3_deps import s3_auth
from urllib.parse import quote_plus


@app.task
def create_catalog(bucket_name: str, name_catalog: str):
    s3 = s3_auth()

    catalog_key = f"{name_catalog}"

    try:
        s3.put_object(Bucket=bucket_name, Key=catalog_key)
        catalog_url = f"https://{bucket_name}.s3.amazonaws.com/{quote_plus(catalog_key)}"
        catalog_data = {
            "catalog_name": name_catalog,
            "catalog_url": catalog_url,
            "status": "created"
        }

        return catalog_data

    except Exception as e:
        return f"error: {str(e)}"
