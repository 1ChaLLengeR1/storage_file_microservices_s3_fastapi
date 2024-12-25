from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import FileResponse
from endpoints.routers import DOWNLOAD_FILE
from consumer.handler.files.download import handler_download_file
from endpoints.response import response_data
import time
import os
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData

router = APIRouter()


@router.get(DOWNLOAD_FILE)
async def download_file(background_tasks: BackgroundTasks, request: Request, file_id: str, ):
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

    task = handler_download_file.delay(file_id, bucket_name, key_main)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, True)

    if response['is_valid'] and response['status'] == "SUCCESS":
        file_path = response['data']['file_path']
        if file_path and os.path.exists(file_path):
            return FileResponse(path=file_path, media_type=response['data']['mime_type'],
                                filename=response['data']['file'])

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
