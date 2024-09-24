from fastapi import APIRouter, BackgroundTasks
from consumer.services.s3.collection import collection_buckets, collection_catalogs, collection_one
from endpoints.routers import COLLECTION_BUCKETS, COLLECTION_CATALOGS, COLLECTION_ONE_FILES
from pydantic import BaseModel

router = APIRouter()


class CollectionOneFile(BaseModel):
    name_bucket: str
    name_file: str


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


@router.post(COLLECTION_ONE_FILES)
async def get_collection_files(background_tasks: BackgroundTasks, collection_one_file: CollectionOneFile):
    task = collection_one.delay(collection_one_file.name_bucket, collection_one_file.name_file)
    background_tasks.add_task(task.wait)
    return {"task_id": task.id}
