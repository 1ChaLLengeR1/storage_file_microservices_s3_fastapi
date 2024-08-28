from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from config.celery_config import app
from endpoints.routers import TASK_ID

router = APIRouter()

@router.get(TASK_ID)
async def get_task_status(task_id: str):
    task_result = app.AsyncResult(task_id)




    if task_result.state == 'PENDING':
        return {
            "status": "Pending",
            "status_code": status.HTTP_202_ACCEPTED
        }

    elif task_result.state == 'SUCCESS':
        return {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "result":task_result.result
        }

    elif task_result.state == 'FAILURE':
        return {
            "status": "failure",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "result": task_result.result
        }
    else:
        return {
            "status": task_result.state,
            "status_code": status.HTTP_400_BAD_REQUEST,
            "result": task_result.result
        }