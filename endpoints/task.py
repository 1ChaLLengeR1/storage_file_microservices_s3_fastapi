from fastapi import APIRouter, status, Response
from config.celery_config import app
from endpoints.routers import TASK_ID

router = APIRouter()


@router.get(TASK_ID)
async def get_task_status(task_id: str, response: Response):
    task_result = app.AsyncResult(task_id)

    if task_result.state == 'PENDING':
        response.status_code = status.HTTP_202_ACCEPTED
        return {
            "status": "PENDING",
            "status_code": status.HTTP_202_ACCEPTED,
            "result": None
        }

    if task_result.state == 'SUCCESS':
        if hasattr(task_result.result, 'error') and task_result.result.error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "status": "ERROR",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "result": task_result.result

            }

        response.status_code = status.HTTP_200_OK

        return {
            "status": "SUCCESS",
            "status_code": status.HTTP_200_OK,
            "result": task_result.result
        }

    elif task_result.state == 'FAILURE':
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "FAILURE",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "result": task_result.result
        }
