import asyncio

from fastapi import BackgroundTasks
from celery.result import AsyncResult
import time
from consumer.data.response import ResponseData


async def response_data(
        background_tasks: BackgroundTasks,
        task,
        timeout,
        start_time,
        pending_wait: bool = False
) -> ResponseData:
    if not task or not task.id:
        raise ValueError("Niepoprawne ID zadania")

    try:
        if pending_wait:
            while True:
                task_result = AsyncResult(task.id)
                if task_result.state == 'SUCCESS':
                    return ResponseData(
                        is_valid=task_result.result['is_valid'],
                        data=task_result.result['data'],
                        status_code=task_result.result['status_code'],
                        status=task_result.result['status']
                    )

                await asyncio.sleep(2)

        while (time.time() - start_time) < timeout:
            task_result = AsyncResult(task.id)

            if task_result.state == 'SUCCESS':
                return ResponseData(
                    is_valid=task_result.result['is_valid'],
                    data=task_result.result['data'],
                    status_code=task_result.result['status_code'],
                    status=task_result.result['status']
                )

            await asyncio.sleep(1)  # Czekanie przed następną iteracją

        background_tasks.add_task(task.wait)
        return ResponseData(
            is_valid=True,
            data={"task_id": task.id},
            status_code=202,
            status="PENDING"
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            data={"error": str(e)},
            status_code=500,
            status="FAILURE"
        )
