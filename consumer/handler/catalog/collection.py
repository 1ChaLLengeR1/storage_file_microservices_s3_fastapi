from database.database import get_db
from database.modals.Catalog.models import Catalog
from config.celery_config import app
from sqlalchemy.exc import SQLAlchemyError
from consumer.data.error import ResponseError
from consumer.handler.authorization.authorization import authorization_main


@app.task(serializer="pickle")
def handler_collection_catalog(name_bucket: str, key_main: str):
    try:

        db_gen = get_db()
        db = next(db_gen)

        check_authorization = authorization_main(key_main, db)
        if not check_authorization.verify:
            return ResponseError(error=check_authorization.message)

        data = db.query(Catalog).filter(Catalog.bucketName == name_bucket).all()

        if len(data) == 0:
            return ResponseError(error="lack catalogs or s3 storage not exist")

        sorted_data = sorted(data, key=lambda x: x.path)

        folder_tree = {}

        for entry in sorted_data:
            folder_path = entry.path
            parts = folder_path.strip("/").split("/")
            current_node = folder_tree

            for part in parts[:-1]:

                if part not in current_node:
                    current_node[part] = {
                        "subfolders": {}
                    }
                current_node = current_node[part]["subfolders"]

            folder_name = parts[-1]
            current_node[folder_name] = {
                "id": entry.id,
                "bucketName": entry.bucketName,
                "name": entry.name,
                "originalName": entry.originalName,
                "path": entry.path,
                "url": entry.url,
                "level": entry.level,
                "subfolders": {}
            }

        return folder_tree


    except SQLAlchemyError as e:
        db.rollback()
        return ResponseError(error=f"Database error: {str(e)}")

    except Exception as e:
        return ResponseError(error=f"{str(e)}")

    finally:
        db.close()
