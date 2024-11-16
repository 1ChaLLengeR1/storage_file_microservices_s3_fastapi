from database.database import get_db
from database.modals.Catalog.models import Catalog
from config.celery_config import app
from sqlalchemy.exc import SQLAlchemyError
from consumer.data.error import ResponseError
# from consumer.handler.authorization.authorization import authorization_main
from consumer.services.s3.download import download_s3_catalog

from config.config_app import DOWNLOAD_FOLDER
from consumer.helper.files import clear_folders_and_zips, zip_catalog


@app.task(serializer="pickle")
def handler_download_catalog(catalog_id: str, bucket_name: str, key_main: str):
    try:
        db_gen = get_db()
        db = next(db_gen)

        paths = []

        # check_authorization = authorization_main(key_main, db)
        # if not check_authorization.verify:
        #     return ResponseError(error=check_authorization.message)

        catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog:
            return ResponseError(error="catalog id is not exist in database")

        path_to_download = catalog.path
        related_catalogs = db.query(Catalog).filter(Catalog.path.like(f"{path_to_download}%")).all()

        for related_catalog in related_catalogs:
            catalog_name = related_catalog.originalName
            catalog_path = related_catalog.path
            paths.append({
                "name": catalog_name,
                "path": catalog_path
            })

            download_s3_catalog(bucket_name, catalog_path)

        if paths:
            main_catalog_path = DOWNLOAD_FOLDER / paths[0]['path']
            zip_file_path = f"{zip_catalog(main_catalog_path)}.zip"

        clean_up_task.apply_async(args=[DOWNLOAD_FOLDER], countdown=5)
        return {"success": "Download Successful", "zip_file": str(zip_file_path)}


    except SQLAlchemyError as e:
        db.rollback()
        return ResponseError(error=f"Database error: {str(e)}")

    except Exception as e:
        return ResponseError(error=f"{str(e)}")

    finally:
        db.close()


@app.task(serializer="pickle")
def clean_up_task(directory):
    """Task to clean up folder and remove zip files after 5 seconds"""
    print(f"Cleaning up {directory}...")
    # Perform the cleaning action
    clear_folders_and_zips(directory)
