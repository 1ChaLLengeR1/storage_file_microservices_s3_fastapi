from database.database import get_db
from database.modals.Catalog.models import Catalog
from consumer.data.response import ResponseData
from sqlalchemy.exc import SQLAlchemyError
from consumer.repository.authorization.psql.auth import authorization_main
from consumer.services.s3.delete import delete_catalog


def delete_catalog_psql(catalog_id: str, bucket_name: str, key_main: str) -> ResponseData:
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

        catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": "catalog id is not exist in database"},
                status_code=400,
            )

        path_to_delete = catalog.path
        related_catalogs = db.query(Catalog).filter(Catalog.path.like(f"{path_to_delete}%")).all()

        serialized_catalogs = [
            {
                "id": catalog.id,
                "bucketName": catalog.bucketName,
                "path": catalog.path,
                "url": catalog.url,
                "level": catalog.level,
                "name": catalog.name,
                "originalName": catalog.originalName
            }
            for catalog in related_catalogs
        ]

        unique_levels = {cat.level for cat in related_catalogs}
        min_level = min(unique_levels, default=None)

        catalog_main = next((cat for cat in related_catalogs if cat.level == min_level), None)

        delete_catalog_s3 = delete_catalog(bucket_name, catalog_main.path)
        if delete_catalog_s3.error:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                status_code=401,
                data={"error": str(delete_catalog_s3)}
            )

        db.query(Catalog).filter(Catalog.path.like(f"{path_to_delete}%")).delete(synchronize_session=False)
        db.commit()

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=serialized_catalogs
        )

    except SQLAlchemyError as e:
        db.rollback()
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
