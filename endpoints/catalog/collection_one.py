from fastapi import APIRouter, BackgroundTasks, Request, status, Response
from fastapi.responses import JSONResponse
from endpoints.routers import COLLECTION_ONE_CATALOG
from consumer.handler.catalog.collection_one import handler_collection_one_catalog
from celery.result import AsyncResult
import time
import asyncio

router = APIRouter()


@router.get(COLLECTION_ONE_CATALOG)
async def get_collection_catalog(background_tasks: BackgroundTasks, request: Request, id: str, response: Response):
    key_main = request.headers.get("key_main")
    if not key_main:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_main' in headers"}
        )

    task = handler_collection_one_catalog.delay(id, key_main)
    timeout = 10
    start_time = time.time()
    try:
        while (time.time() - start_time) < timeout:
            task_result = AsyncResult(task.id)
            if task_result.state == 'SUCCESS':
                if hasattr(task_result.result, 'error') and task_result.result.error:
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {
                        "status": "ERROR",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "result": task_result.result
                    }

                response.status_code = status.HTTP_200_OK
                return {
                    "status": "SUCCESS",
                    "status_code": status.HTTP_200_OK,
                    "result": task_result.result
                }
            await asyncio.sleep(0.5)
    except Exception as e:
        return {
            "status": "FAILURE",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "result": {"error": str(e)}
        }

    background_tasks.add_task(task.wait)
    return {
        "status": "PENDING",
        "status_code": status.HTTP_202_ACCEPTED,
        "result": {"task_id": task.id}
    }
