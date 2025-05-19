from fastapi import FastAPI, Request, Body
from loguru import logger
import uvicorn

app = FastAPI(title="LLM Backend API")

@app.post("/ask_llm_and_get_response")
async def trigger_task(request: Request, question: str = Body(...)):
   
    return {"response": "Hello"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080) 