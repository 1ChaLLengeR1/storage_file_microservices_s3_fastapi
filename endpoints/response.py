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
                if not task_result.result['is_valid']:
                    return ResponseData(
                        is_valid=task_result.result['is_valid'],
                        data=task_result.result['data'],
                        status_code=task_result.result['status_code'],
                        status=task_result.result['status']
                    )

                return ResponseData(
                    is_valid=task_result.result['is_valid'],
                    data=task_result.result['data'],
                    status_code=task_result.result['status_code'],
                    status=task_result.result['status']
                )
    except Exception as e:
        return ResponseData(
            is_valid=False,
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
