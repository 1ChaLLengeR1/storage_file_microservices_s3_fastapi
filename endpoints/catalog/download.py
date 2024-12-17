from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import FileResponse
from endpoints.routers import DOWNLOAD_CATALOG
from consumer.handler.catalog.download import handler_download_catalog
from endpoints.response import response_data
import time
import os
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData

router = APIRouter()


@router.get(DOWNLOAD_CATALOG)
async def download_catalog(background_tasks: BackgroundTasks, id: str, request: Request):
    bucket_name = request.query_params.get("bucket_name")
    if not bucket_name:
        if not bucket_name:
            return ResponseApiData(
                status="ERROR",
                data={"error": "Missing 'bucket_name' in query parameters"},
                status_code=400
            ).to_response()

    required_headers = ["key_main"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code']
        ).to_response()

    key_main = data_header['data'][0]['data']

    task = handler_download_catalog.delay(id, bucket_name, key_main)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, True)

    if response['is_valid'] and response['status'] == "SUCCESS":
        zip_file_path = response['data']['zip_file_path']
        if zip_file_path and os.path.exists(zip_file_path):
            return FileResponse(path=zip_file_path, media_type='application/zip', filename="storage_s3_files.zip")

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
