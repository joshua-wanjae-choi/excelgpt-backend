from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.query import router as query_router
from controller.file import router as file_router
from config.llm_model import LLMModel
from util.db import DB
import sys

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


app.include_router(query_router)
app.include_router(file_router)
