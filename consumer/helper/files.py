import os
import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile
from consumer.data.response import ResponseData

from config.config_app import DOWNLOAD_FOLDER, TMP_FOLDER


def save_files_tmp(upload_files: List[UploadFile]) -> List[str] | dict:
    try:

        tmp_dir = TMP_FOLDER
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        saved_files = []
        for upload_file in upload_files:
            file_path = os.path.join(tmp_dir, upload_file.filename)
            with open(file_path, "wb") as tmp_file:
                content = upload_file.file.read()
                tmp_file.write(content)

            os.chmod(file_path, 0o777)
            saved_files.append(file_path)

        return saved_files

    except Exception as e:
        return {"error": str(e)}


def check_files_size(upload_files: List[UploadFile]) -> int:
    sum_size = 0
    for upload_file in upload_files:
        sum_size += upload_file.size

    return sum_size


def clear_tmp_files(file_paths: List[str]) -> bool:
    try:
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
        return True
    except Exception as e:
        print({"error": str(e)})
        return False


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


def clear_folders_and_zips(directory, all_catalog: bool = False):
    if not os.path.isdir(directory):
        return

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

        elif os.path.isfile(item_path) and all_catalog:
            os.remove(item_path)

        elif os.path.isfile(item_path) and item.endswith('.zip'):
            os.remove(item_path)


ALLOWED_FORMATS = {
    "jpg", "jpeg", "png", "gif", "webp", "svg",
    "pdf", "txt", "doc", "docx", "md", "csv",
    "mp3", "wav", "mp4", "mov", "json"
}


def validate_file_extensions(files: list[str]) -> ResponseData:
    try:
        invalid_files = []
        for file_path in files:
            file_name = Path(file_path).name
            file_extension = file_name.split('.')[-1].lower()

            if file_extension not in ALLOWED_FORMATS:
                invalid_files.append({
                    "file_name": file_name,
                    "invalid_extension": file_extension,
                    "allowed_formats": list(ALLOWED_FORMATS)
                })

        if len(invalid_files) > 0:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=invalid_files,
                status_code=400
            )

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=[],
            status_code=200
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            status_code=417,
            data={"error": str(e)}
        )
