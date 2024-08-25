from fastapi import APIRouter, BackgroundTasks
from config.celery_config import app
from consumer.services.s3.collection import collection_buckets, collection_catalogs
from endpoints.routers import COLLECTION_BUCKETS, COLLECTION_CATALOGS

router = APIRouter()
@router.get(COLLECTION_BUCKETS)
async def get_collection_buckets(background_tasks: BackgroundTasks):
    task = collection_buckets.apply_async()
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}

@router.get(COLLECTION_CATALOGS)
async def get_collection_catalogs(background_tasks: BackgroundTasks, name_bucket: str):
    task = collection_catalogs.delay(name_bucket, "https://storage-fastapi-s3.s3.eu-north-1.amazonaws.com/")
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = app.AsyncResult(task_id)
    if task_result.state == 'PENDING':
        return {"status": "Pending"}
    elif task_result.state == 'SUCCESS':
        return {"status": "Success", "result": task_result.result}
    else:
        return {"status": task_result.state, "result": str(task_result.info)}
