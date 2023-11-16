from sqlalchemy import create_engine, text
from secret import Secret


class DB:
    engine = create_engine(
        f"mariadb+mariadbconnector://{Secret.db_user}:{Secret.db_password}@{Secret.db_host}:{Secret.db_port}"
    )

    def init_database():
        # 없으면 DB 생성
        with DB.engine.connect() as conn:
            conn.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {Secret.db_database_name}")
            )

            # DB 사용
            conn.execute(text(f"USE {Secret.db_database_name}"))