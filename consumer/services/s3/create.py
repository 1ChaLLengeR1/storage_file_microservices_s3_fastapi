from config.s3_deps import s3_auth
from urllib.parse import quote_plus
from consumer.helper.convert import original_name_from_path
from consumer.data.response import ResponseData


def create_catalog(bucket_name: str, name_catalog: str) -> ResponseData:
    try:

        s3 = s3_auth()
        if not name_catalog.endswith('/'):
            catalog_path = f"{name_catalog}/"
        else:
            catalog_path = name_catalog

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=catalog_path)
        if 'Contents' in response:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": "Folder already exists in S3"},
                status_code=400
            )

        s3.put_object(Bucket=bucket_name, Key=catalog_path)
        catalog_url = f"https://{bucket_name}.s3.amazonaws.com/{quote_plus(catalog_path)}"

        catalog_data = {
            "catalog_name": original_name_from_path(name_catalog),
            "catalog_url": catalog_url,
            "catalog_path": catalog_path,
            "status": "created"
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=catalog_data,
            status_code=200
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=400,
            data={"error": str(e)}
        )
