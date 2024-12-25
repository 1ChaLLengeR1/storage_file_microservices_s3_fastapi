from database.modals.Catalog.models import Catalog
from sqlalchemy.exc import SQLAlchemyError
from database.database import get_db
from consumer.data.response import ResponseData
from consumer.repository.authorization.psql.auth import authorization_main


def collection_catalog_psql(name_bucket: str, key_main: str) -> ResponseData:
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

        data = db.query(Catalog).filter(Catalog.bucketName == name_bucket).all()
        if len(data) == 0:
            return ResponseData(
                status="ERROR",
                is_valid=False,
                data={"error": "lack catalogs or s3 storage not exist"},
                status_code=400,
            )

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

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            status_code=200,
            data=folder_tree
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
