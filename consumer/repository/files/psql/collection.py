from consumer.data.response import ResponseData
from database.database import get_db
from consumer.repository.authorization.psql.auth import authorization_main
from database.modals.File.models import File
from sqlalchemy.exc import SQLAlchemyError


def collection_files_psql(catalog_id: str, key_main: str) -> ResponseData:
    try:
        db_gen = get_db()
        db = next(db_gen)

        check_authorization = authorization_main(key_main, db)
        if not check_authorization['is_valid']:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=check_authorization['data'],
                status_code=check_authorization['status_code'],
            )

        rows_files = db.query(File).filter(File.catalog_id == catalog_id).all()

        files_data = [
            {
                "id": file.id,
                "catalog_id": file.catalog_id,
                "mime_type": file.mime_type,
                "file_name": file.file_name,
                "original_name": file.original_name,
                "file_size": file.file_size,
                "s3_url": file.s3_url,
                "s3_path": file.s3_path,
            }
            for file in rows_files
        ]

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=files_data
        )
    except SQLAlchemyError as e:
        db.rollback()
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data=str(e)
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data=str(e)
        )
    finally:
        db.close()
