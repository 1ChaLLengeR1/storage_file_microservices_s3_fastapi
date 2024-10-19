from fastapi import APIRouter, BackgroundTasks, Request
from endpoints.routers import COLLECTION_CATALOGS
from consumer.handler.catalog.collection import handler_collection_catalog

router = APIRouter()

@router.get(COLLECTION_CATALOGS)
async def get_collection_catalog(background_tasks: BackgroundTasks,  request: Request):
    task = handler_collection_catalog.delay()
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}