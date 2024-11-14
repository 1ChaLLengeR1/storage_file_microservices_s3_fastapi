from fastapi import APIRouter, BackgroundTasks, Request
from endpoints.routers import COLLECTION_ONE_CATALOG
from consumer.handler.catalog.collection_one import handler_collection_one_catalog
from endpoints.response import response_data
import time
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData

router = APIRouter()


@router.get(COLLECTION_ONE_CATALOG)
async def get_collection_catalog(background_tasks: BackgroundTasks, request: Request, id: str):
    required_headers = ["key_main"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code']
        ).to_response()

    key_main = data_header['data'][0]['data']

    task = handler_collection_one_catalog.delay(id, key_main)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
