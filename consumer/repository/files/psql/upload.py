from consumer.data.response import ResponseData
from database.database import get_db
from consumer.repository.authorization.psql.auth import authorization_create
from database.modals.Catalog.models import Catalog
from sqlalchemy.exc import SQLAlchemyError
from consumer.services.s3.create import upload_file
from consumer.helper.files import clear_tmp_files


def upload_file_psql(bucket_name: str, catalog_id: str, key_create: str, files: list[str]) -> ResponseData:
    try:

        db_gen = get_db()
        db = next(db_gen)

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

        clear_tmp_files(files)

        


        data = {
            "id": catalog_records.id
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=data
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
