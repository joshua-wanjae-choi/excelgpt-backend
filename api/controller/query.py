from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from service.answer import get_full_query, get_answer


router = APIRouter(prefix="/query")


class InputQuery(BaseModel):
    data: Dict[str, str] = ""


@router.post("")
async def request_query(input_query: InputQuery):
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

            return {"data": rows}
    except:
        raise HTTPException(status_code=500, detail="failed to run query")
