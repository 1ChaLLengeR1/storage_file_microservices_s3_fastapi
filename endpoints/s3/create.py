from fastapi import APIRouter, BackgroundTasks
from endpoints.routers import CREATE_CATALOG
from consumer.handler.catalog.create import handler_create_catalog
from pydantic import BaseModel

router = APIRouter()

class CreateCatalog(BaseModel):
    catalog_name: str
    bucket_name: str

@router.post(CREATE_CATALOG)
def post_create_catalog(background_tasks: BackgroundTasks, create_catalog_s3: CreateCatalog):
    task = handler_create_catalog.delay(create_catalog_s3.bucket_name, create_catalog_s3.catalog_name)
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}