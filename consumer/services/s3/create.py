from config.s3_deps import s3_auth
from urllib.parse import quote_plus
from consumer.helper.convert import original_name_from_path
from consumer.data.response import ResponseData
from botocore.exceptions import ClientError
import os
import mimetypes
from consumer.helper.random import createRandom


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


def upload_file(bucket_name: str, catalog_path: str, files: list[str]) -> ResponseData:
    try:
        s3 = s3_auth()
        if isinstance(files, str):
            files = [files]
        uploaded_files = []

        for file_path in files:
            if not os.path.isfile(file_path):
                continue

            with open(file_path, 'rb') as file:
                object_name = os.path.basename(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type:
                    mime_type = 'application/octet-stream'

                s3_object_name = createRandom(object_name, 10)
                s3_path = f"{catalog_path}{s3_object_name}"
                s3.put_object(Bucket=bucket_name, Key=s3_path, Body=file.read(),
                              ContentType=mime_type)

                file_data = {
                    "file_name": s3_object_name,
                    "original_name": object_name,
                    "s3_path": s3_path,
                    "mime_type": mime_type,
                    "file_size": os.path.getsize(file_path),
                    "s3_url": f"https://{bucket_name}.s3.amazonaws.com/{s3_path}"
                }

                uploaded_files.append(file_data)

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=uploaded_files
        )

    except ClientError as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=400,
            data={"error": str(e)}
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
