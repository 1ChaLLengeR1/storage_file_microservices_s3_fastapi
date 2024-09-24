from database.database import get_db
from database.modals.Catalog.models import Catalog
from sqlalchemy.exc import SQLAlchemyError
from .data.create import HandlerCatalogResponse
from consumer.services.s3.create import create_catalog
from config.celery_config import app
from consumer.helper.random import createRandom
from consumer.handler.authorization.authorization import authorization_create


@app.task(serializer="pickle")
def handler_create_catalog(bucket_name: str, name_catalog: str, key_create: str) -> HandlerCatalogResponse:
    db_gen = get_db()
    db = next(db_gen)

    try:

        check_authorization = authorization_create(key_create, db)
        if not check_authorization.verify:
            return HandlerCatalogResponse(error=check_authorization.message)

        original_name_catalog: str = name_catalog

        create_catalog_3 = create_catalog(bucket_name, original_name_catalog)
        if create_catalog_3.error:
            return HandlerCatalogResponse(error=str(create_catalog_3.error))

        new_catalog = Catalog(
            bucketName=bucket_name,
            name=createRandom(create_catalog_3.catalog_name, 10),
            originalName=create_catalog_3.catalog_name,
            path=create_catalog_3.catalog_path,
            url=create_catalog_3.catalog_url
        )

        db.add(new_catalog)
        db.commit()
        db.refresh(new_catalog)

        return HandlerCatalogResponse(
            id=new_catalog.id,
            bucketName=new_catalog.bucketName,
            name=new_catalog.name,
            originalName=new_catalog.originalName,
            path=new_catalog.path,
            url=new_catalog.url,
            createUp=new_catalog.createUp,
            updateUp=new_catalog.updateUp
        )


    except SQLAlchemyError as e:
        db.rollback()
        return HandlerCatalogResponse(error=f"Database error: {str(e)}")

    except Exception as e:
        return HandlerCatalogResponse(error=str(e))

    finally:
        db.close()
