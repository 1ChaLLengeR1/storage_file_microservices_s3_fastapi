import shutil
from pathlib import Path

from config.config_app import DOWNLOAD_FOLDER

def create_catalog_folder(relative_path: str):
    catalog_dir = DOWNLOAD_FOLDER / relative_path
    try:
        catalog_dir.mkdir(parents=True, exist_ok=True)
        return catalog_dir

    except Exception as e:
        return {"error": str(e)}


def zip_catalog(catalog_dir: Path):
    zip_file_path = DOWNLOAD_FOLDER / catalog_dir.name
    try:
        shutil.make_archive(zip_file_path, 'zip', str(catalog_dir), '.')
        return zip_file_path
    except Exception as e:
        return {"error": str(e)}