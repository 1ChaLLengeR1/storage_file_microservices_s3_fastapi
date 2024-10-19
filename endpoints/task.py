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
        return JSONResponse(
            content={
                "status": "PENDING",
                "status_code": status.HTTP_202_ACCEPTED,
                "result": None
            },
            status_code=status.HTTP_202_ACCEPTED
        )

    elif 'error' in task_result.result and task_result.result['error'] and task_result.state == 'SUCCESS':
        return JSONResponse(
            content={
                "status": "ERROR",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "result": task_result.result.__dict__
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    elif task_result.state == 'SUCCESS':
        return {
            "status": "SUCCESS",
            "status_code": status.HTTP_200_OK,
            "result": task_result.result
        }

    elif task_result.state == 'FAILURE':
        return JSONResponse(
            content={
                "status": "FAILURE",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": None
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
