from celery import Celery
import os
import sys
from pipelines.config.ap_config import broker_url, result_backend

app = Celery(
    "LLM App",
    broker=broker_url,
    backend=result_backend,
    include=["pipelines.server.celery_app.tasks"])

# Avoid prefetching
app.conf.update(
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
    task_acks_late=True
)
