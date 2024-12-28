from fastapi import APIRouter, BackgroundTasks, Request, UploadFile, File, Form
from endpoints.routers import UPLOAD_FILES, CREATE_UPLOAD
from consumer.handler.files.upload import handler_upload_file, handler_create_upload
from endpoints.response import response_data
import time
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData
from consumer.helper.files import save_files_tmp, check_files_size
from consumer.helper.files import clear_tmp_files

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

    if check_files_size(file) > 0:
        response_save_files = save_files_tmp(file)
    else:
        response_save_files = []

    task = handler_upload_file.delay(name_bucket, catalog_id, key_create, response_save_files)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, True)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()


@router.post(CREATE_UPLOAD)
async def upload_create(
        background_tasks: BackgroundTasks,
        request: Request,
        name_bucket: str,
        name_catalog: str = Form(...),
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

    if check_files_size(file) > 0:
        response_save_files = save_files_tmp(file)
    else:
        response_save_files = []

    print(response_save_files)

    task = handler_create_upload.delay(name_bucket, name_catalog, response_save_files, key_create)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, True)
    clear_tmp_files(response_save_files)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
