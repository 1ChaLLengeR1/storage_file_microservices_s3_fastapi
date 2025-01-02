from consumer.data.response import ResponseData
from database.database import get_db
from consumer.repository.authorization.psql.auth import authorization_create
from database.modals.Catalog.models import Catalog
from database.modals.File.models import File
from sqlalchemy.exc import SQLAlchemyError
from consumer.services.s3.create import upload_file
from consumer.helper.files import clear_tmp_files


def upload_file_psql(bucket_name: str, catalog_id: str, key_create: str, files: list[str],
                     remove_one: bool = True) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        created_files = []

        check_authorization = authorization_create(key_create, db)
        if not check_authorization['is_valid']:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=check_authorization['data'],
                status_code=check_authorization['status_code'],
            )

        catalog_records = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog_records:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": f"Not found catalog with this id: {catalog_id}"},
                status_code=400,
            )

        response_upload = upload_file(bucket_name, catalog_records.path, files)
        if not response_upload['is_valid']:
            return ResponseData(
                is_valid=response_upload['is_valid'],
                status=response_upload['status'],
                data=response_upload['data'],
                status_code=response_upload['status_code'],
            )
        if remove_one:
            clear_tmp_files(files)

        for file in response_upload['data']:
            new_file = File(
                catalog_id=catalog_id,
                mime_type=file['mime_type'],
                file_name=file['file_name'],
                original_name=file['original_name'],
                file_size=file['file_size'],
                s3_url=file['s3_url'],
                s3_path=file['s3_path']
            )

            db.add(new_file)
            db.commit()
            db.refresh(new_file)
            created_files.append(new_file)

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
                "createUp": str(file.createUp),
                "updateUp": str(file.updateUp),
            }
            for file in created_files
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
