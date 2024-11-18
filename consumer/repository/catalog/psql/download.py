from database.database import get_db
from consumer.data.response import ResponseData
from sqlalchemy.exc import SQLAlchemyError
from consumer.repository.authorization.psql.auth import authorization_main
from database.modals.Catalog.models import Catalog
from config.config_app import DOWNLOAD_FOLDER
from consumer.helper.files import clear_folders_and_zips, zip_catalog
from consumer.services.s3.download import download_s3_catalog


def download_catalog_psql(catalog_id: str, bucket_name: str, key_main: str) -> ResponseData:
    try:
        db_gen = get_db()
        db = next(db_gen)
        paths = []

        check_authorization = authorization_main(key_main, db)
        if not check_authorization['is_valid']:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=check_authorization['data'],
                status_code=check_authorization['status_code'],
            )

        catalog = db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data={"error": "catalog id is not exist in database"},
                status_code=check_authorization['status_code'],
            )

        path_to_download = catalog.path
        related_catalogs = db.query(Catalog).filter(Catalog.path.like(f"{path_to_download}%")).all()
        response = None

        for related_catalog in related_catalogs:
            catalog_name = related_catalog.originalName
            catalog_path = related_catalog.path
            paths.append({
                "name": catalog_name,
                "path": catalog_path
            })

            response_download = download_s3_catalog(bucket_name, catalog_path)
            if not response_download['is_valid']:
                return ResponseData(
                    is_valid=response_download['is_valid'],
                    status=response_download['status'],
                    status_code=response_download['status_code'],
                    data=response_download['data']
                )
            response = response_download

        if paths:
            main_catalog_path = DOWNLOAD_FOLDER / paths[0]['path']
            zip_file_path = f"{zip_catalog(main_catalog_path)}.zip"

            data = {
                "global_catalog": response['data']['global_catalog'],
                "last_catalog": response['data']['last_catalog'],
                "path_remove": str(DOWNLOAD_FOLDER),
                "zip_file_path": zip_file_path
            }

            return ResponseData(
                is_valid=True,
                status="SUCCESS",
                status_code=200,
                data=data
            )

        return ResponseData(
            is_valid=False,
            status="Error",
            status_code=400,
            data={"error": "no catalog to download"}
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
