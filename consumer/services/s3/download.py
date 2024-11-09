import os
from config.s3_deps import s3_auth
from pydantic import BaseModel
from typing import Optional
from botocore.exceptions import ClientError
from config.config_app import DOWNLOAD_FOLDER


class S3CatalogResponse(BaseModel):
    error: Optional[str] = None


def download_s3_catalog(bucket_name: str, path_catalog: str) -> S3CatalogResponse:
    try:
        s3 = s3_auth()
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=path_catalog)
        if 'Contents' in response:
            local_folder = os.path.join(DOWNLOAD_FOLDER, path_catalog)
            os.makedirs(local_folder, exist_ok=True)
            for obj in response['Contents']:
                s3_object_key = obj['Key']
                if not s3_object_key.endswith('/'):
                    relative_path = os.path.relpath(s3_object_key,
                                                    path_catalog)
                    local_file_path = os.path.join(local_folder, relative_path)
                    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                    s3.download_file(bucket_name, s3_object_key, local_file_path)

        else:
            print("Brak obiektów do pobrania.")

        return S3CatalogResponse(error=None)
    except ClientError as e:
        return S3CatalogResponse(error=str(e))
    except Exception as e:
        return S3CatalogResponse(error=str(e))
