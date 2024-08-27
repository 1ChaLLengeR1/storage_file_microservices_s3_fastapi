from fastapi import APIRouter
from endpoints.s3.collection import router as s3_collection_router
from endpoints.s3.create import router as s3_create_router
from endpoints.tast import router as task_router

api_router = APIRouter()

api_router.include_router(s3_collection_router)
api_router.include_router(s3_create_router)
api_router.include_router(task_router)

