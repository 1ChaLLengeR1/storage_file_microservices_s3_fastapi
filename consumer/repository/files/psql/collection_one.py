from consumer.data.response import ResponseData
from database.database import get_db
from consumer.repository.authorization.psql.auth import authorization_main
from database.modals.File.models import File
from sqlalchemy.exc import SQLAlchemyError


def collection_one_file_psql(file_id: str, key_main: str) -> ResponseData:
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

        row_file = db.query(File).filter(File.id == file_id).first()
        if not row_file:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": f"Not found file with this id: {file_id}"},
                status_code=400,
            )

        file_obj = {
            "id": row_file.id,
            "catalog_id": row_file.catalog_id,
            "mime_type": row_file.mime_type,
            "file_name": row_file.file_name,
            "original_name": row_file.original_name,
            "file_size": row_file.file_size,
            "s3_url": row_file.s3_url,
            "s3_path": row_file.s3_path,
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=file_obj
        )

    except SQLAlchemyError as e:
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
