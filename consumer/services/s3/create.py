from config.s3_deps import s3_auth
from urllib.parse import quote_plus
from pydantic import BaseModel
from typing import Optional

class S3CatalogResponse(BaseModel):
    catalog_name: Optional[str] = None
    catalog_url: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None


def create_catalog(bucket_name: str, name_catalog: str) -> S3CatalogResponse:
    try:

        s3 = s3_auth()
        catalog_key = f"{name_catalog}/"

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=catalog_key)
        if 'Contents' in response:
            return S3CatalogResponse(error="Folder already exists")

        s3.put_object(Bucket=bucket_name, Key=catalog_key)
        catalog_url = f"https://{bucket_name}.s3.amazonaws.com/{quote_plus(catalog_key)}"
        catalog_data = S3CatalogResponse(
            catalog_name=name_catalog,
            catalog_url=catalog_url,
            status="created"
        )

        return catalog_data

    except Exception as e:
        return S3CatalogResponse(error=str(e))
