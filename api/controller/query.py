from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Union
from model.query_count_by_ip import QueryCountByIp
from service.answer import get_full_query, get_answer
from datetime import datetime


router = APIRouter(prefix="/query")


class InputQuery(BaseModel):
    data: Dict[str, str] = ""


@router.post("")
async def request_query(
    input_query: InputQuery,
    x_forwarded_for: Union[str, None] = Header(default=None),
):
    home_dir_path = "/home/excelgpt/app"
    disk_dir_path = f"{home_dir_path}/disk"
    userspace_name = "my_user"
    userspace_path = f"{disk_dir_path}/{userspace_name}"
    result_file_name = "result"
    result_path = f"{userspace_path}/{result_file_name}"
    num_ref_lines = 5

    if "query" not in input_query.data:
        raise HTTPException(status_code=422, detail="query not found")

    is_ok, error_code, result = get_full_query(
        userspace_path=userspace_path,
        result_file_name=result_file_name,
        num_ref_lines=num_ref_lines,
        query=input_query.data["query"],
    )

    if not is_ok:
        raise HTTPException(status_code=error_code, detail=result)

    full_query = result
    is_ok, result = get_answer(full_query=full_query)
    if not is_ok:
        raise HTTPException(status_code=500, detail="failed to run query")

    try:
        source = result
        if is_ok:
            exec(source)

            rows = []
            with open(result_path) as f:
                rows = f.read().splitlines()

            # 쿼리 카운트 갱신
            ip = x_forwarded_for
            _update_query_count(ip)

            return {"data": rows}
    except:
        raise HTTPException(status_code=500, detail="failed to run query")


def _update_query_count(ip: str):
    today_date = datetime.utcnow().strftime("%Y-%m-%d")
    query_count_result = QueryCountByIp.retrieve_query_count(ip, today_date)
    if query_count_result is None:
        QueryCountByIp.init_query_count(ip, today_date)

    else:
        QueryCountByIp.update_query_count(
            ip, today_date, query_count_result.query_count + 1
        )
