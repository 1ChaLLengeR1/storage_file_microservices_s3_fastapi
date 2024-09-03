from config.s3_deps import s3_auth
from urllib.parse import quote_plus
from pydantic import BaseModel
from typing import Optional
from consumer.helper.convert import original_name_from_path

class S3CatalogResponse(BaseModel):
    catalog_name: Optional[str] = None
    catalog_url: Optional[str] = None
    catalog_path: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None


def create_catalog(bucket_name: str, name_catalog: str) -> S3CatalogResponse:
    try:

        s3 = s3_auth()
        if not name_catalog.endswith('/'):
            catalog_path = f"{name_catalog}/"
        else:
            catalog_path = name_catalog


        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=catalog_path)
        if 'Contents' in response:
            return S3CatalogResponse(error="Folder already exists")

        s3.put_object(Bucket=bucket_name, Key=catalog_path)
        catalog_url = f"https://{bucket_name}.s3.amazonaws.com/{quote_plus(catalog_path)}"
        catalog_data = S3CatalogResponse(
            catalog_name=original_name_from_path(name_catalog),
            catalog_url=catalog_url,
            catalog_path=catalog_path,
            status="created"
        )

        return catalog_data

    except Exception as e:
        return S3CatalogResponse(error=str(e))
