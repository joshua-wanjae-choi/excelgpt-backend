# excelgpt-backend
excelgpt-backend

### 개발서버 실행
- ```bash
    # api로 이동
    cd ~/api

    # fastAPI 개발서버 실행
    uvicorn main:app_fastapi --reload --host=0.0.0.0 --port=8000
    # 또는
    uvicorn api:app --reload --host=0.0.0.0 --port=8000

    # rocketry와 fastAPI 함께 실행
    python main.py
    ```

### 참고
- PaLM 가이드
    - https://developers.generativeai.google/tutorials/text_quickstart
- rocketry: Integrate FastAPI
    - https://rocketry.readthedocs.io/en/stable/cookbook/fastapi.html
