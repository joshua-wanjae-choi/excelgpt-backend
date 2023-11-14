import os

class Config:
    limit_query_count = int(os.getenv('LIMIT_QUERY_COUNT', "100"))
    days_expired_files = int(os.getenv('DAYS_EXPIRED_FILES', "1"))
    disk_dir_name = os.getenv('DISK_DIR_NAME', "disk")
