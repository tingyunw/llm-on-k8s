from fastapi import FastAPI, Request, Body
from loguru import logger
import uvicorn
from pipelines.server.celery_app.tasks import ask_ollma_task


app = FastAPI(title="LLM Backend API")

@app.post("/ask_llm_and_get_response")
async def trigger_task(request: Request, question: str = Body(...)):
    result = ask_ollma_task.delay(question)
    return {"response": result.get()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080) 