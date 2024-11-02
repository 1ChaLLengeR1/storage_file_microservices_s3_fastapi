from database.database import get_db
from database.modals.Catalog.models import Catalog
from config.celery_config import app
from sqlalchemy.exc import SQLAlchemyError
from consumer.data.error import ResponseError
from consumer.handler.authorization.authorization import authorization_main


def handler_delete_catalog(catalog_id: str, key_main: str):
    try:
        db_gen = get_db()
        db = next(db_gen)

        check_authorization = authorization_main(key_main, db)
        if not check_authorization.verify:
            return ResponseError(error=check_authorization.message)

        data = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not data:
            return ResponseError(error="catalog id is not exist in database")

        return "Usunięto"


    except SQLAlchemyError as e:
        db.rollback()
        return ResponseError(error=f"Database error: {str(e)}")

    except Exception as e:
        return ResponseError(error=f"{str(e)}")

    finally:
        db.close()
