from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from model.query_count_by_ip import QueryCountByIp
from config.config import Config
from datetime import datetime
from config.response import Response


class LimitQueryCountByIP(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        ip = request.headers["x-forwarded-for"]
        today_date = datetime.utcnow().strftime("%Y-%m-%d")

        query_count_result = QueryCountByIp.retrieve_query_count(ip, today_date)
        if (
            query_count_result is not None
            and query_count_result.query_count > Config.limit_query_count
        ):
            content = Response.get_response("3000")
            return JSONResponse(status_code=500, content=content)

        response = await call_next(request)
        return response
