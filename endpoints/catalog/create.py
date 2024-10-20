from fastapi import APIRouter, BackgroundTasks, Request
from endpoints.routers import CREATE_CATALOG
from fastapi.responses import JSONResponse
from consumer.handler.catalog.create import handler_create_catalog
from pydantic import BaseModel

router = APIRouter()

class CreateCatalog(BaseModel):
    catalog_name: str
    bucket_name: str

@router.post(CREATE_CATALOG)
async def post_create_catalog(background_tasks: BackgroundTasks, create_catalog_s3: CreateCatalog, request: Request):
    key_create = request.headers.get("key_create")
    if not key_create:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_create' in headers"}
        )

    task = handler_create_catalog.delay(create_catalog_s3.bucket_name, create_catalog_s3.catalog_name, key_create)
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}