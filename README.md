# excelgpt-backend
excelgpt-backend

### 개발서버 실행
- ```bash
    # api로 이동
    cd ~/api

    # fastAPI 개발서버와 스케줄러 실행
    uvicorn main:app --reload --host=0.0.0.0 --port=8000 --lifespan on
    # fastAPI 개발서버만 실행
    uvicorn main:app --reload --host=0.0.0.0 --port=8000
    ```

### 참고
- PaLM 가이드
    - https://developers.generativeai.google/tutorials/text_quickstart
- rocketry: Integrate FastAPI
    - https://rocketry.readthedocs.io/en/stable/cookbook/fastapi.html
