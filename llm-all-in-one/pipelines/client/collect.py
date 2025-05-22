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
from io import StringIO, BytesIO
from minio import Minio

with open('/home/almalinux/miniopass', 'r') as f:
    minio_secret_key = f.read().strip()

minio_client = Minio(
    "localhost:9000",
    access_key = "myminioadmin",
    secret_key = minio_secret_key,
    secure = True,
    cert_check = False
)

def upload_dataframe_to_minio(df, bucket_name, object_name):

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode('utf-8')
    
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created.")

    minio_client.put_object(
        bucket_name,
        object_name,
        data=BytesIO(csv_bytes),
        length=len(csv_bytes),
        content_type="text/csv"
    )


def get_original_question_and_answer(task_id):
    with open(f"submitted_jobs/{task_id}.txt", "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    return lines[0], lines[1]


def collect_answers():

    Path("results").mkdir(parents=True, exist_ok=True)

    start_time, duration = time(), 25 * 60 * 60
    batch_cnt = 0

    while time() - start_time < duration:

        results = []
        jobs = [f.name for f in Path("submitted_jobs").iterdir() if f.is_file()]

        for i in jobs:
            celery_task_id = i.split(".")[0]
            query_params = {
                "celery_task_id": celery_task_id,
            }

            with requests.get(f"{router_url}/get_llm_response", params=query_params) as response:
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json["status"] == "done":
                        question, answer = get_original_question_and_answer(celery_task_id)

                        logger.info(f"Question: {question}")
                        logger.info(f"Ollama Response: {res_json['answer']}")

                        results.append({
                            "question": question,
                            "response": res_json["answer"],
                            # "answer": answer,
                        })
                    else:
                        logger.info(f"{celery_task_id} is: {res_json['status']}")
                        continue
                else:
                    logger.error("Failed:", response.status_code, response.text)
                    Path("failed_jobs").mkdir(parents=True, exist_ok=True)
                    Path(f"failed_jobs/{i}").touch()

            Path(f"submitted_jobs/{i}").unlink()

        if results:
            batch_cnt += 1
            result_df = pd.DataFrame(results)
            upload_dataframe_to_minio(result_df, "analysis-results", f"batch_{batch_cnt}_results.csv")
            # result_df.to_csv(f"results/batch_{batch_cnt}_results.csv", index=False)

        sleep(1800)


if __name__ == "__main__":

    collect_answers()
