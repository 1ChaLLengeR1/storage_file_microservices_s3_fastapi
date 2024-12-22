from config.s3_deps import s3_auth
from pydantic import BaseModel
from typing import Optional
from botocore.exceptions import ClientError
from consumer.data.response import ResponseData


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


def delete_files(bucket_name: str, list_path: list[str]):
    try:
        s3 = s3_auth()
        deleted_files = []
        error_files = []
        paginator = s3.get_paginator('list_objects_v2')
        for path_catalog in list_path:
            for page in paginator.paginate(Bucket=bucket_name, Prefix=path_catalog):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        try:
                            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                            deleted_files.append(obj['Key'])
                        except Exception as e:
                            error_files.append({
                                "key": obj['Key'],
                                "file_path": path_catalog,
                                "message": str(e)
                            })

        if len(error_files) > 0:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=error_files,
                status_code=400
            )

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=deleted_files,
            status_code=200
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data={"error": str(e)},
            status_code=417
        )
