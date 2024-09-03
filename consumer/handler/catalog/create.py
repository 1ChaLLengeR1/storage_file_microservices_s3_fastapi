from database.database import get_db
from database.modals.Catalog.models import Catalog
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from consumer.services.s3.create import create_catalog
from config.celery_config import app
from consumer.helper.random import createRandom
class HandlerCatalogResponse(BaseModel):
    id: Optional[str] = None
    bucketName: Optional[str] = None
    name: Optional[str] = None
    originalName: Optional[str] = None
    path: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    createUp: Optional[datetime] = None
    updateUp: Optional[datetime] = None
@app.task(serializer="pickle")
def handler_create_catalog(bucket_name: str, name_catalog: str,) -> HandlerCatalogResponse:

    db_gen = get_db()
    db = next(db_gen)
    original_name_catalog: str = name_catalog
    name: str = createRandom(name_catalog, 10)

    try:

        create_catalog_3 = create_catalog(bucket_name, original_name_catalog)
        if create_catalog_3.error:
            return HandlerCatalogResponse(error=str(create_catalog_3.error))

        new_catalog = Catalog(
            bucketName=bucket_name,
            name=name,
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





