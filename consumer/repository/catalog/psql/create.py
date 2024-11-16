from database.modals.Catalog.models import Catalog
from sqlalchemy.exc import SQLAlchemyError
from database.database import get_db
from consumer.data.response import ResponseData
from consumer.helper.random import createRandom
from consumer.helper.convert import path_lvl, split_path
from consumer.services.s3.create import create_catalog
from consumer.repository.authorization.psql.auth import authorization_create


def create_catalog_psql(bucket_name: str, name_catalog: str, key_create: str) -> ResponseData:
    try:
        db_gen = get_db()
        db = next(db_gen)

        check_authorization = authorization_create(key_create, db)
        if not check_authorization['is_valid']:
            return ResponseData(
                status="ERROR",
                data=check_authorization['data'],
                status_code=check_authorization['status_code'],
            )

        original_name_catalog: str = name_catalog
        split_paths = split_path(original_name_catalog)
        catalog_records = db.query(Catalog).filter(Catalog.path.in_(split_paths)).all()
        last_path = split_paths[-1]
        created_catalogs = []

        for index, catalog in enumerate(catalog_records):
            if catalog.path == last_path:
                return ResponseData(
                    is_valid=False,
                    status="ERROR",
                    data={"error": "catalog exist in database"},
                    status_code=400,
                )

        existing_paths = {record.path for record in catalog_records}
        for path in split_paths:
            if path in existing_paths:
                continue
            else:
                create_catalog_3 = create_catalog(bucket_name, path)
                if create_catalog_3.error:
                    return ResponseData(
                        is_valid=False,
                        status="ERROR",
                        data={"error": "catalog exist in database"},
                        status_code=400,
                    )

                new_catalog = Catalog(
                    bucketName=bucket_name,
                    name=createRandom(create_catalog_3.catalog_name, 10),
                    originalName=create_catalog_3.catalog_name,
                    path=create_catalog_3.catalog_path,
                    url=create_catalog_3.catalog_url,
                    level=path_lvl(path)
                )

                db.add(new_catalog)
                db.commit()
                db.refresh(new_catalog)
                created_catalogs.append(new_catalog)

        catalog_data = [
            {
                "id": catalog.id,
                "bucketName": catalog.bucketName,
                "name": catalog.name,
                "originalName": catalog.originalName,
                "path": catalog.path,
                "url": catalog.url,
                "level": catalog.level,
                "createUp": str(catalog.createUp),
                "updateUp": str(catalog.updateUp),
            }
            for catalog in created_catalogs
        ]

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=catalog_data
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
