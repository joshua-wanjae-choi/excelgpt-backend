from model.query_count_by_ip import QueryCountByIp
from config.config import Config
import pathlib
import os
import shutil


async def clean_expired_files():
    print("run")
    api_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
    disk_dir_path = f"{api_path}/{Config.disk_dir_name}"

    list_expired_ip_result = QueryCountByIp.list_expired_ip(Config.days_expired_files)
    for row in list_expired_ip_result:
        userspace_name = row.ip
        userspace_path = f"{disk_dir_path}/{userspace_name}"
        try:
            if os.path.exists(userspace_path):
                shutil.rmtree(userspace_path)
        except Exception as e:
            pass
