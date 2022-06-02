# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging

from celery import Celery
from src.config import settings

logger = logging.getLogger(__name__)
app = Celery(
    broker=f"{settings.BASE_CELERY_BROKER_URL}/{settings.CORONER_SERVICE_NAME}",
    result_backend=settings.CELERY_RESULT_URL,
    task_acks_late=True,
    celery_queue_ha_policy="all",
    broker_connection_retry=True,
)


# celery --app=tests.mini_coroner worker --concurrency=1 -E --loglevel=INFO
# --queues=inference-function


@app.task(
    bind=True,
    queue=settings.INFERENCE_QUEUE,
    name=settings.CORONER_INFERENCE,
    task_reject_on_worker_lost=True,
    autoretry_for=(Exception,),
    acks_late=True,
    retry_backoff=True,
    max_retries=3,
    task_time_limit=8
)
def foo(
        self,
        data
):
    print(data)

    return {
        "x": [{"value": "12121", "trustful": False}, {
            "value":
                "120",
            "trustful": True}],
        "y": [{"value": "100", "trustful": True}],
        "z": [],
        "unit": [{"value": "cm", "trustful": True},
                 {"value": "cm", "trustful": True}]}
