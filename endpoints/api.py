from fastapi import APIRouter
from endpoints.s3.collection import router as s3_collection_router
from endpoints.catalog.create import router as catalog_create_router
from endpoints.task import router as task_router

api_router = APIRouter()

api_router.include_router(s3_collection_router)
api_router.include_router(catalog_create_router)
api_router.include_router(task_router)

