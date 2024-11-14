from fastapi import APIRouter, BackgroundTasks, Request
from endpoints.routers import CREATE_CATALOG
from consumer.handler.catalog.create import handler_create_catalog
from pydantic import BaseModel
from endpoints.response import response_data
import time
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData

router = APIRouter()


class CreateCatalog(BaseModel):
    catalog_name: str
    bucket_name: str


@router.post(CREATE_CATALOG)
async def post_create_catalog(background_tasks: BackgroundTasks, create_catalog_s3: CreateCatalog, request: Request):
    required_headers = ["key_create"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code']
        ).to_response()

    key_create = data_header['data'][0]['data']

    task = handler_create_catalog.delay(create_catalog_s3.bucket_name, create_catalog_s3.catalog_name, key_create)

    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
