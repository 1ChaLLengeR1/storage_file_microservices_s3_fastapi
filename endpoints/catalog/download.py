from fastapi import APIRouter, BackgroundTasks, Request, Response
from fastapi.responses import JSONResponse, FileResponse
from endpoints.routers import DOWNLOAD_CATALOG
from consumer.handler.catalog.download import handler_download_catalog
from endpoints.response import response_data
import time
import os

router = APIRouter()


@router.get(DOWNLOAD_CATALOG)
async def download_catalog(background_tasks: BackgroundTasks, id: str, request: Request, response: Response):
    bucket_name = request.query_params.get("bucket_name")
    if not bucket_name:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'bucket_name' in query parameters"}
        )

    key_main = request.headers.get("key_main")
    if not key_main:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_main' in headers"}
        )

    task = handler_download_catalog.delay(id, bucket_name, key_main)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, response)

    if response.get("status") == "SUCCESS":
        zip_file_path = response["result"].get("zip_file")
        if zip_file_path and os.path.exists(zip_file_path):
            return FileResponse(path=zip_file_path, media_type='application/zip', filename="storage_s3_files.zip")

    return response
