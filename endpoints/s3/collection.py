from fastapi import APIRouter, BackgroundTasks
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

    folder_prefix = 'test1/'

    task = collection_catalogs.delay(name_bucket, folder_prefix)
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}


