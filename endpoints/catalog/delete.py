from fastapi import APIRouter, BackgroundTasks, Request, Response
from endpoints.routers import DELETE_CATALOG
from consumer.handler.catalog.delete import handler_delete_catalog
from endpoints.response import response_data
import time
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData

router = APIRouter()


@router.delete(DELETE_CATALOG)
async def delete_catalog(background_tasks: BackgroundTasks, id: str, request: Request):
    bucket_name = request.query_params.get("bucket_name")
    if not bucket_name:
        return ResponseApiData(
            status="ERROR",
            data={"error": "Missing 'bucket_name' in query parameters"},
            status_code=400
        ).to_response()

    required_headers = ["key_delete"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code']
        ).to_response()

    key_delete = data_header['data'][0]['data']

    task = handler_delete_catalog.delay(id, bucket_name, key_delete)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
