from util.secret_util import SecretUtil
import pathlib

# secret 파일 로드
api_path = str(pathlib.Path(__file__).parent.resolve())
secret_path = f"{api_path}/secret.py"
docker_secret_name = "api-secret"
SecretUtil.load_secret(secret_path=secret_path, docker_secret_name=docker_secret_name)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler import AsyncScheduler
from controller.query import router as query_router
from controller.file import router as file_router
from config.llm_model import LLMModel
from middleware.apscheduler import SchedulerMiddlerware
from middleware.limit_query_count_ip import LimitQueryCountByIP
from util.db import DB
import sys

# api 경로 sys.path에 추가
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
app.add_middleware(LimitQueryCountByIP)

scheduler = AsyncScheduler()
app.add_middleware(SchedulerMiddlerware, scheduler=scheduler)


# 라우터 설정
@app.get("/health-check")
async def health_check():
    return {"data": "success"}


app.include_router(query_router)
app.include_router(file_router)
