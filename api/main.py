from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config.llm_model import LLMModel
from controller.query import router as query_router
from pydantic import BaseModel
from typing import Dict
from util.db import DB
import google.generativeai as palm
import os
import sys
import re

# api 경로 sys.path에 추가
api_path = "/home/excelgpt/app/api"
sys.path.append(api_path)

# fastAPI app 로드
app = FastAPI()

# LLM Model 초기화
LLMModel.init()

# DB 초기화
DB.init_database()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def health_check():
    return {"data": "success"}


class InputFile(BaseModel):
    data: Dict[str, str] = []


class InputQuery(BaseModel):
    data: Dict[str, str] = ""


def extract_source(raw: str):
    pattern = re.compile("```python(.*)```", re.DOTALL)
    found = pattern.findall(raw)

    if len(found) > 0:
        return True, found[0]

    return False, ""


@app.post("/file")
async def file(input_file: InputFile):
    home_dir_path = "/home/excelgpt/app"
    disk_dir_path = f"{home_dir_path}/disk"
    userspace_name = "my_user"
    userspace_path = f"{disk_dir_path}/{userspace_name}"

    os.makedirs(userspace_path, exist_ok=True)

    for file_name in input_file.data:
        file_path = f"{userspace_path}/{file_name}"
        contents = input_file.data[file_name]
        with open(file_path, "w") as f:
            f.write(contents)

    return {"data": "success"}


@app.post("/query")
async def query(input_query: InputQuery):
    home_dir_path = "/home/excelgpt/app"
    disk_dir_path = f"{home_dir_path}/disk"
    userspace_name = "my_user"
    userspace_path = f"{disk_dir_path}/{userspace_name}"
    result_file_name = "result"
    result_path = f"{userspace_path}/{result_file_name}"
    num_ref_lines = 5

    if "query" not in input_query.data:
        raise HTTPException(status_code=422, detail="query not found")

    file_names = os.listdir(userspace_path)
    file_names = [
        file_name for file_name in file_names if file_name != result_file_name
    ]
    if len(file_names) < 0:
        raise HTTPException(status_code=404, detail="files not found")

    full_query = ""
    for file_name in file_names:
        lines = ""
        path = f"{userspace_path}/{file_name}"
        with open(path) as f:
            for _ in range(num_ref_lines):
                lines += f.readline()
            f.close()

        chunk = f"""dataframe name is {file_name}.
file path is "{path}".
data of {file_name} = `
{lines}
`.
first line of {file_name} is header.
delimiter of {file_name} is "|".
extension of {file_name} not exists.
index_col of {file_name} is False.
        
"""
        if lines != "":
            full_query += chunk

        full_query += f"""

result dataframe is named {result_file_name}.
result file path is {result_path}.
delimiter of {result_file_name} is "|".
result file of extension not exists.

request below.
{input_query.data['query']}
Extract only existing columns of sheet2.

constraints below.
using python, pandas and do not print results.

"""
        completion = palm.generate_text(
            model=LLMModel.model,
            prompt=full_query,
            temperature=0,
            max_output_tokens=800,
        )
        print(f"${full_query=}")
        print(f"${completion.result=}")
        is_ok, source = extract_source(completion.result)
        if not is_ok:
            raise HTTPException(status_code=500, detail="failed to run query")

        try:
            if is_ok:
                exec(source)

                rows = []
                with open(result_path) as f:
                    rows = f.read().splitlines()
                    
                return {"data": rows}
        except:
            raise HTTPException(status_code=500, detail="failed to run query")


app.include_router(query_router)
