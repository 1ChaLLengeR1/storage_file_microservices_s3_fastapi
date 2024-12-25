from consumer.data.response import ResponseData
from database.database import get_db
from consumer.repository.authorization.psql.auth import authorization_delete
from database.modals.File.models import File
from sqlalchemy.exc import SQLAlchemyError
from consumer.services.s3.delete import delete_files


def delete_files_psql(bucket_name: str, list_id: list[str], key_delete: str) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:

        check_authorization = authorization_delete(key_delete, db)
        if not check_authorization['is_valid']:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=check_authorization['data'],
                status_code=check_authorization['status_code'],
            )

        rows_files = db.query(File).filter(File.id.in_(list_id)).all()

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

        files_path_data = [
            file.s3_path
            for file in rows_files
        ]

        response_delete_s3 = delete_files(bucket_name, files_path_data)
        if not response_delete_s3['is_valid']:
            return ResponseData(
                is_valid=response_delete_s3['is_valid'],
                status=response_delete_s3['status'],
                data={"error": response_delete_s3['data']},
                status_code=response_delete_s3['status_code']
            )

        db.query(File).filter(File.id.in_(list_id)).delete(synchronize_session=False)
        db.commit()

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=files_data,
            status_code=200
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


def delete_files_all(catalog_id: str) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:

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

        db.query(File).filter(File.catalog_id == catalog_id).delete(synchronize_session=False)
        db.commit()

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=files_data,
            status_code=200
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
