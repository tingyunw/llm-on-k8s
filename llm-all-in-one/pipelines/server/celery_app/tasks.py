from celery.result import AsyncResult
import os
import sys
from pipelines.server.celery_app.app import app
from pipelines.server.celery_app.utils.call_llm import call_ollama

@app.task(bind=True)
def ask_ollma_task(self, question):
    return call_ollama(question, "deepseek-r1:1.5B")


def get_ollama_response(celery_task_id):
    result = AsyncResult(celery_task_id, app=app)
    if result.ready():
        return result.get()
