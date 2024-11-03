from config.s3_deps import s3_auth
from pydantic import BaseModel
from typing import Optional
from botocore.exceptions import ClientError


class S3CatalogResponse(BaseModel):
    error: Optional[str] = None


def delete_catalog(bucket_name: str, path_catalog: str) -> S3CatalogResponse:
    try:
        s3 = s3_auth()
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=path_catalog):
            if 'Contents' in page:
                for obj in page['Contents']:
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])

        return S3CatalogResponse(error=None)
    except ClientError as e:
        return S3CatalogResponse(error=str(e))
    except Exception as e:
        return S3CatalogResponse(error=str(e))
