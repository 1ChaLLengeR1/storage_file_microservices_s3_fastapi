from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from endpoints.routers import COLLECTION_ONE_CATALOG
from consumer.handler.catalog.collection_one import handler_collection_one_catalog

router = APIRouter()

@router.get(COLLECTION_ONE_CATALOG)
async def get_collection_catalog(background_tasks: BackgroundTasks, request: Request, id: str):
    key_main = request.headers.get("key_main")
    if not key_main:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing 'key_main' in headers"}
        )

    task = handler_collection_one_catalog.delay(id, key_main)
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}