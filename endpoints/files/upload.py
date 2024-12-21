from fastapi import APIRouter, BackgroundTasks, Request, UploadFile, File, Form
from endpoints.routers import UPLOAD_FILES
from consumer.handler.files.upload import handler_upload_file
from endpoints.response import response_data
import time
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData
from consumer.helper.files import save_files_tmp

router = APIRouter()


@router.post(UPLOAD_FILES)
async def upload_files(
        background_tasks: BackgroundTasks,
        request: Request,
        name_bucket: str,
        catalog_id: str = Form(...),
        file: list[UploadFile] = File(...),
):
    required_headers = ["key_create"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code']
        ).to_response()

    key_create = data_header['data'][0]['data']

    response_save_files = save_files_tmp(file)

    task = handler_upload_file.delay(name_bucket, catalog_id, key_create, response_save_files)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, True)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
