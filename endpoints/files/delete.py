from fastapi import APIRouter, BackgroundTasks, Request
from consumer.helper.header import check_required_headers
from consumer.data.response import ResponseApiData
from endpoints.routers import DELETE_FILES
from consumer.handler.files.delete import handler_delete_files
from endpoints.response import response_data
import time
from pydantic import BaseModel

router = APIRouter()


class DeleteFiles(BaseModel):
    collection_id: list[str]


@router.delete(DELETE_FILES)
async def collection_files(
        background_tasks: BackgroundTasks,
        request: Request,
        name_bucket: str,
        collection_id: DeleteFiles
):
    required_headers = ["key_delete"]
    data_header = check_required_headers(request, required_headers)
    if not data_header['is_valid']:
        return ResponseApiData(
            status="ERROR",
            data=data_header['data'],
            status_code=data_header['status_code']
        ).to_response()

    key_delete = data_header['data'][0]['data']

    task = handler_delete_files.delay(name_bucket, collection_id.collection_id, key_delete)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time)

    return ResponseApiData(
        status=response["status"],
        data=response["data"],
        status_code=response["status_code"]
    ).to_response()
