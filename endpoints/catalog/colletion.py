from fastapi import APIRouter, BackgroundTasks, Request, status, Response
from fastapi.responses import JSONResponse
from endpoints.routers import COLLECTION_CATALOGS
from consumer.handler.catalog.collection import handler_collection_catalog
from endpoints.response import response_data
import time

router = APIRouter()


@router.get(COLLECTION_CATALOGS)
async def get_collection_catalog(background_tasks: BackgroundTasks, request: Request, name_bucket: str,
                                 response: Response):
    key_main = request.headers.get("key_main")
    if not key_main:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_main' in headers"}
        )

    task = handler_collection_catalog.delay(name_bucket, key_main)
    timeout = 10
    start_time = time.time()

    response = await response_data(background_tasks, task, timeout, start_time, response)
    return response
