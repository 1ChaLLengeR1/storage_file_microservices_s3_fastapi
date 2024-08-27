from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from config.celery_config import app
from endpoints.routers import TASK_ID

router = APIRouter()

@router.get(TASK_ID)
async def get_task_status(task_id: str):
    task_result = app.AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return JSONResponse(
            content={"status": "Pending"},
            status_code=status.HTTP_202_ACCEPTED
        )
    elif task_result.state == 'SUCCESS':
        return JSONResponse(
            content={"status": "success", "status_code": "200", "result": task_result.result},
            status_code=status.HTTP_200_OK
        )
    elif task_result.state == 'FAILURE':
        return JSONResponse(
            content={"status": "failure", "status_code": "500", "result": str(task_result.info)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return JSONResponse(
            content={"status": task_result.state, "result": str(task_result.info)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
