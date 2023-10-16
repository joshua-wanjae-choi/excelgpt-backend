from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.llm_model import LLMModel
from controller.query import router as query_router
import sys

# api 경로 sys.path에 추가
api_path = "/home/excelgpt/app/api"
sys.path.append(api_path)

# fastAPI app 로드
app = FastAPI()

# LLM Model 초기화
LLMModel.init()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def root():
    return {"data": "success"}


@app.post("/file")
async def file():
    return {"data": "success"}


app.include_router(query_router)
