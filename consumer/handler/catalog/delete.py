from database.database import get_db
from database.modals.Catalog.models import Catalog
from config.celery_config import app
from sqlalchemy.exc import SQLAlchemyError
from consumer.data.error import ResponseError
# from consumer.handler.authorization.authorization import authorization_main
from consumer.services.s3.delete import delete_catalog
from config.redis_client import delete_cache_by_prefix


@app.task(serializer="pickle")
def handler_delete_catalog(catalog_id: str, bucket_name: str, key_main: str):
    try:
        db_gen = get_db()
        db = next(db_gen)

        # check_authorization = authorization_main(key_main, db)
        # if not check_authorization.verify:
        #     return ResponseError(error=check_authorization.message)

        catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog:
            return ResponseError(error="catalog id is not exist in database")

        path_to_delete = catalog.path
        related_catalogs = db.query(Catalog).filter(Catalog.path.like(f"{path_to_delete}%")).all()

        unique_levels = {cat.level for cat in related_catalogs}
        min_level = min(unique_levels, default=None)

        catalog_main = next((cat for cat in related_catalogs if cat.level == min_level), None)

        delete_catalog_s3 = delete_catalog(bucket_name, catalog_main.path)
        if delete_catalog_s3.error:
            return {"error": delete_catalog_s3}

        for related_catalog in related_catalogs:
            db.delete(related_catalog)

        db.commit()
        delete_cache_by_prefix("catalog_")
        return related_catalogs


    except SQLAlchemyError as e:
        db.rollback()
        return ResponseError(error=f"Database error: {str(e)}")

    except Exception as e:
        return ResponseError(error=f"{str(e)}")

    finally:
        db.close()
