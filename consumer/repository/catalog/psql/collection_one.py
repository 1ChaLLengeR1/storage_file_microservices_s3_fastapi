from database.modals.Catalog.models import Catalog
from sqlalchemy.exc import SQLAlchemyError
from database.database import get_db
from consumer.data.response import ResponseData
from consumer.repository.authorization.psql.auth import authorization_main


def collection_one_catalog_psql(catalog_id: str, key_main: str) -> ResponseData:
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

        data = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not data:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": "catalog id is not exist in database"},
                status_code=400,
            )
        sub_catalogs = db.query(Catalog).filter(Catalog.path.like(f"{data.path}%"),
                                                Catalog.level == data.level + 1).all()

        sub_catalog_list = [
            {
                "id": sub.id,
                "level": sub.level,
                "originalName": sub.originalName,
                "path": sub.path,
                "url": sub.url
            }
            for sub in sub_catalogs
        ]

        result = {
            "id": data.id,
            "bucketName": data.bucketName,
            "originalName": data.originalName,
            "name": data.name,
            "level": data.level,
            "path": data.path,
            "url": data.url,
            "sub_catalogs": sub_catalog_list
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=result
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
