from fastapi import APIRouter, BackgroundTasks, Request, status, Response
from endpoints.routers import CREATE_CATALOG
from fastapi.responses import JSONResponse
from consumer.handler.catalog.create import handler_create_catalog
from pydantic import BaseModel
from celery.result import AsyncResult
import time
import asyncio

router = APIRouter()


class CreateCatalog(BaseModel):
    catalog_name: str
    bucket_name: str


@router.post(CREATE_CATALOG)
async def post_create_catalog(background_tasks: BackgroundTasks, create_catalog_s3: CreateCatalog, request: Request,
                              response: Response):
    key_create = request.headers.get("key_create")
    if not key_create:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_create' in headers"}
        )

    task = handler_create_catalog.delay(create_catalog_s3.bucket_name, create_catalog_s3.catalog_name, key_create)

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
