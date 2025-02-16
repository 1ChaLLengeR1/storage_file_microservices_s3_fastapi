from fastapi import APIRouter

from endpoints.catalog.create import router as catalog_create_router
from endpoints.catalog.colletion import router as catalog_collection_router
from endpoints.catalog.collection_one import router as catalog_collection_one_router
from endpoints.catalog.delete import router as catalog_delete
from endpoints.catalog.download import router as download_catalog
from endpoints.task import router as task_router
from endpoints.files.upload import router as upload_files
from endpoints.files.collection import router as collection_files
from endpoints.files.delete import router as delete_files
from endpoints.files.collection_one import router as collection_one_file
from endpoints.files.download import router as download_file
from endpoints.files.upload import router as handler_create_upload

api_router = APIRouter()

api_router.include_router(catalog_create_router)
api_router.include_router(catalog_delete)
api_router.include_router(download_catalog)
api_router.include_router(catalog_collection_router)
api_router.include_router(catalog_collection_one_router)
api_router.include_router(task_router)
api_router.include_router(upload_files)
api_router.include_router(collection_files)
api_router.include_router(collection_one_file)
api_router.include_router(delete_files)
api_router.include_router(download_file)
api_router.include_router(handler_create_upload)
