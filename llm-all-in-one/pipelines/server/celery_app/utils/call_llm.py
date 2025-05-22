from loguru import logger
from ollama import chat

logger.remove()  # Remove default handler
logger.add(lambda msg: print(msg, end="", flush=True), format="{message}")

def call_ollama(question, model="deepseek-r1:1.5B", streaming=False):
    response = chat(
        model=model,
        messages=[
        {
            'role': 'user',
            'content': question,
        }],
        # options={
        #     'num_predict': 10,
        # },
        stream=streaming,
    )

    if streaming:
        full_message = ""
        for chunk in response:
            logger.info(chunk['message']['content'])
            full_message += chunk['message']['content']
        return full_message
    else:
        return response['message']['content'].split("</think>")[-1]
