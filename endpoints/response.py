from fastapi import status, Response, BackgroundTasks
from celery.result import AsyncResult
import time
import asyncio


async def response_data(background_tasks: BackgroundTasks, task, timeout, start_time, response: Response):
    try:
        while (time.time() - start_time) < timeout:
            task_result = AsyncResult(task.id)
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
            await asyncio.sleep(0.5)
    except Exception as e:
        return {
            "status": "FAILURE",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "result": {"error": str(e)}
        }

    background_tasks.add_task(task.wait)
    return {
        "status": "PENDING",
        "status_code": status.HTTP_202_ACCEPTED,
        "result": {"task_id": task.id}
    }
