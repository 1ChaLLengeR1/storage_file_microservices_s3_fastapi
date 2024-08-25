from fastapi import APIRouter
from endpoints.s3.collection import router as s3_router

api_router = APIRouter()

api_router.include_router(s3_router)

