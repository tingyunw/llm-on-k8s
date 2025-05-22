import urllib.parse
from time import sleep, time
from pathlib import Path
import requests
import pandas as pd
from loguru import logger
import os
import sys
os.chdir('/home/almalinux/pipelines')
sys.path.insert(0, os.getcwd())
from config.ap_config import router_url

def load_jsonl(jsonl_path):
    return pd.read_json(jsonl_path, lines=True)


def submit_jobs(test=False):
    path_params = dict()

    Path("submitted_jobs").mkdir(parents=True, exist_ok=True)

    if not test:
        df = load_jsonl("/home/almalinux/mathdata.jsonl")

    start_time, duration = time(), 24 * 60 * 60
    idx = 0
    limit = 10000

    while time() - start_time < duration and idx < 10000:

        if test:
            path_params["question"] = "Hi"
        else:
            path_params["question"] = df.iloc[idx]["question"]

        with requests.post(f"{router_url}/ask_llm", data=path_params) as response:
            if response.status_code == 200:
                celery_task_id = response.json()
                logger.info(f"Celery task id: {celery_task_id}")
                with open(f"submitted_jobs/{celery_task_id}.txt", "w") as file:
                    file.write(f"{path_params['question']}\n")
                    file.write(f"{df.iloc[idx]['expected_answer']}\n")
            else:
                logger.error("Failed:", response.status_code, response.text)
                raise ValueError
        idx += 1

        sleep(15)
    
    print('The number of submitted questions: ' + str(idx))


if __name__ == "__main__":

    submit_jobs()

