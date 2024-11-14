from fastapi import BackgroundTasks
from celery.result import AsyncResult
import time
from consumer.data.response import ResponseData
import asyncio


async def response_data(background_tasks: BackgroundTasks, task, timeout, start_time) -> ResponseData:
    try:
        while (time.time() - start_time) < timeout:
            task_result = AsyncResult(task.id)
            if task_result.state == 'SUCCESS':
                if hasattr(task_result.result, 'error') and task_result.result.error:
                    return ResponseData(
                        is_valid=False,
                        data=task_result.result,
                        status_code=400,
                        status="ERROR"
                    )

                return ResponseData(
                    is_valid=True,
                    data=task_result.result,
                    status_code=200,
                    status="SUCCESS"
                )
    except Exception as e:
        return ResponseData(
            is_valid=True,
            data={"error": str(e)},
            status_code=500,
            status="FAILURE"
        )

    background_tasks.add_task(task.wait)
    return ResponseData(
        is_valid=True,
        data={"task_id": task.id},
        status_code=202,
        status="PENDING"
    )
