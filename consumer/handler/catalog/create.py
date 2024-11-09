from database.database import get_db
from database.modals.Catalog.models import Catalog
from sqlalchemy.exc import SQLAlchemyError
from .data.create import HandlerCatalogResponse
from consumer.helper.convert import original_name_from_path
from consumer.data.error import ResponseError
from consumer.services.s3.create import create_catalog
from config.celery_config import app
from consumer.helper.random import createRandom
from consumer.helper.convert import path_lvl, split_path
from consumer.handler.authorization.authorization import authorization_create
from config.redis_client import delete_cache_by_prefix


@app.task(serializer="pickle")
def handler_create_catalog(bucket_name: str, name_catalog: str, key_create: str):
    try:

        db_gen = get_db()
        db = next(db_gen)

        check_authorization = authorization_create(key_create, db)
        if not check_authorization.verify:
            return ResponseError(error=check_authorization.message)

        original_name_catalog: str = name_catalog

        split_paths = split_path(original_name_catalog)
        catalog_records = db.query(Catalog).filter(Catalog.path.in_(split_paths)).all()
        last_path = split_paths[-1]
        created_catalogs = []

        for index, catalog in enumerate(catalog_records):
            if catalog.path == last_path:
                return ResponseError(error="catalog exist in database")

        existing_paths = {record.path for record in catalog_records}
        for path in split_paths:
            if path in existing_paths:
                continue
            else:
                create_catalog_3 = create_catalog(bucket_name, path)
                if create_catalog_3.error:
                    return ResponseError(error=str(create_catalog_3.error))

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

        delete_cache_by_prefix("collection_catalog_")

        return [HandlerCatalogResponse(
            id=catalog.id,
            bucketName=catalog.bucketName,
            name=catalog.name,
            originalName=catalog.originalName,
            path=catalog.path,
            url=catalog.url,
            level=catalog.level,
            createUp=str(catalog.createUp),
            updateUp=str(catalog.updateUp)
        ) for catalog in created_catalogs]

    except SQLAlchemyError as e:
        db.rollback()
        return ResponseError(error=f"Database error: {str(e)}")

    except Exception as e:
        return ResponseError(error=str(e))

    finally:
        db.close()
