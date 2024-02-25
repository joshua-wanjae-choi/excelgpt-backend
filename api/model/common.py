from sqlalchemy.orm import DeclarativeBase
from secret import Secret


class Base(DeclarativeBase):
    __table_args__ = ({"schema": Secret.db_database_name},)

    @staticmethod
    def get_default_schema():
        return {"schema": Secret.db_database_name}
