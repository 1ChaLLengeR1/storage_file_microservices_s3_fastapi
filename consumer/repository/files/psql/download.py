from consumer.data.response import ResponseData
from database.database import get_db
from consumer.repository.authorization.psql.auth import authorization_main
from database.modals.File.models import File
from sqlalchemy.exc import SQLAlchemyError
from consumer.helper.files import zip_catalog
from config.config_app import DOWNLOAD_FOLDER
from consumer.services.s3.download import download_s3_file


def download_file_psql(file_id: str, bucket_name: str, key_main: str) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        check_authorization = authorization_main(key_main, db)
        if not check_authorization['is_valid']:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=check_authorization['data'],
                status_code=check_authorization['status_code'],
            )

        row_file = db.query(File).filter(File.id == file_id).first()
        if not row_file:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": f"Not found file with this id: {file_id}"},
                status_code=400,
            )

        response_download = download_s3_file(bucket_name, row_file.original_name, row_file.s3_path)
        if not response_download['is_valid']:
            return ResponseData(
                is_valid=response_download['is_valid'],
                status=response_download['status'],
                status_code=response_download['status_code'],
                data=response_download['data']
            )
        response = response_download

        if response:
            main_file_path = DOWNLOAD_FOLDER / row_file.original_name
            data = {
                "file": row_file.original_name,
                "mime_type": row_file.mime_type,
                "file_path": str(main_file_path),
                "path_remove": str(DOWNLOAD_FOLDER),
            }

            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                status_code=200,
                data=data
            )

        return ResponseData(
            is_valid=False,
            status="Error",
            status_code=400,
            data={"error": "no file to download"}
        )

    except SQLAlchemyError as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
    finally:
        db.close()
