from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Union
from model.query_count_by_ip import QueryCountByIp
from service.answer import get_full_query, get_answer
from datetime import datetime
from config.config import Config
from config.response import Response
import pathlib


router = APIRouter(prefix="/query")


class InputRow(BaseModel):
    query: str
    base_sheet_name: str


class InputQuery(BaseModel):
    data: InputRow


@router.post("")
async def request_query(
    input_query: InputQuery,
    x_forwarded_for: Union[str, None] = Header(default=None),
):
    home_dir_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
    disk_dir_path = f"{home_dir_path}/{Config.disk_dir_name}"
    userspace_name = x_forwarded_for
    userspace_path = f"{disk_dir_path}/{userspace_name}"
    result_file_name = "result"
    result_path = f"{userspace_path}/{result_file_name}"
    num_ref_lines = 5

    is_ok, status_code, result = get_full_query(
        userspace_path=userspace_path,
        result_file_name=result_file_name,
        num_ref_lines=num_ref_lines,
        query=input_query.data.query,
        base_sheet_name=input_query.data.base_sheet_name,
    )

    if not is_ok:
        content = Response.get_response(result)
        raise HTTPException(status_code=status_code, detail=content)

    full_query = result
    print(f"${full_query=}")

    is_ok, result = get_answer(full_query=full_query)
    if not is_ok:
        content = Response.get_response("7100")
        raise HTTPException(status_code=500, detail=content)
        
    try:
        source = result
        print(f"${source=}")
        if is_ok:
            exec(source)

            rows = []
            with open(result_path) as f:
                rows = f.read().splitlines()

            # 쿼리 카운트 갱신
            ip = x_forwarded_for
            _update_query_count(ip)

            return {"data": rows}
    except Exception as e:
        print(f"${e=}")
        content = Response.get_response("7101")
        raise HTTPException(status_code=500, detail=content)


def _update_query_count(ip: str):
    today_date = datetime.utcnow().strftime("%Y-%m-%d")
    query_count_result = QueryCountByIp.retrieve_query_count(ip, today_date)
    if query_count_result is None:
        QueryCountByIp.init_query_count(ip)

    else:
        QueryCountByIp.update_query_count(
            ip, today_date, query_count_result.query_count + 1
        )
