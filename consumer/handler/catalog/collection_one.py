from config.redis_client import get_cache_data, set_cache_data
from database.database import get_db
from database.modals.Catalog.models import Catalog
from config.celery_config import app
from sqlalchemy.exc import SQLAlchemyError
from consumer.data.error import ResponseError
from consumer.handler.authorization.authorization import authorization_main

@app.task(serializer="pickle")
def handler_collection_one_catalog(catalog_id: str, key_main: str):

    cache_key = f"catalog_{catalog_id}"
    cached_data = get_cache_data(cache_key)
    if cached_data:
        return cached_data

    try:
        db_gen = get_db()
        db = next(db_gen)

        check_authorization = authorization_main(key_main, db)
        if not check_authorization.verify:
            return ResponseError(error=check_authorization.message)

        data = db.query(Catalog).filter(Catalog.id == catalog_id).first()

        if not data:
            return ResponseError(error="catalog id is not exist in database")

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

        set_cache_data(cache_key, result)
        return result

    except SQLAlchemyError as e:
        db.rollback()
        return ResponseError(error=f"Database error: {str(e)}")

    except Exception as e:
        return ResponseError(error=f"{str(e)}")

    finally:
        db.close()
