from fastapi import APIRouter, BackgroundTasks, Request, Response
from fastapi.responses import JSONResponse
from endpoints.routers import DELETE_CATALOG
from consumer.handler.catalog.delete import handler_delete_catalog
from endpoints.response import response_data
import time

router = APIRouter()


@router.delete(DELETE_CATALOG)
async def delete_catalog(background_tasks: BackgroundTasks, id: str, request: Request, response: Response):
    bucket_name = request.query_params.get("bucket_name")
    if not bucket_name:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'bucket_name' in query parameters"}
        )

    key_main = request.headers.get("key_delete")
    if not key_main:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_delete' in headers"}
        )

    task = handler_delete_catalog.delay(id, bucket_name, key_main)
    timeout = 10
    start_time = time.time()
    response = await response_data(background_tasks, task, timeout, start_time, response)
    return response
