from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
import os


router = APIRouter(prefix="/file")


class InputFile(BaseModel):
    data: Dict[str, str] = []


@router.post("")
def async_file(input_file: InputFile):
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
