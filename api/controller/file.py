from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import Dict, Union
from config.config import Config
from config.response import Response
import pathlib
import os


router = APIRouter(prefix="/file")


class InputFile(BaseModel):
    data: Dict[str, str] = []


@router.post("")
def async_file(
    input_file: InputFile,
    x_forwarded_for: Union[str, None] = Header(default=None),
):
    try:
        home_dir_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        disk_dir_path = f"{home_dir_path}/{Config.disk_dir_name}"
        userspace_name = x_forwarded_for
        userspace_path = f"{disk_dir_path}/{userspace_name}"
        os.makedirs(userspace_path, exist_ok=True)

        for file_name in input_file.data:
            file_path = f"{userspace_path}/{file_name}"
            contents = input_file.data[file_name]
            with open(file_path, "w") as f:
                f.write(contents)

        return Response.get_response("0000")
    except Exception as e:
        print(f"${e=}")
        return Response.get_response("7000")
