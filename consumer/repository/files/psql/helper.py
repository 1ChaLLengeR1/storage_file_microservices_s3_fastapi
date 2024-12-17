from fastapi import UploadFile
from consumer.data.response import ResponseData

ALLOWED_FORMATS = {
    "jpg", "jpeg", "png", "gif", "webp", "svg",
    "pdf", "txt", "doc", "docx", "md", "csv",
    "mp3", "wav", "mp4", "mov", "json"
}


def validate_file_extensions(files: list[UploadFile]) -> ResponseData:
    try:
        invalid_files = []
        for file in files:
            file_name = file.filename
            if not file_name:
                continue

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