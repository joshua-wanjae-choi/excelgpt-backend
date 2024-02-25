from model.common import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import (
    String,
    BigInteger,
    DateTime,
    select,
    insert,
    update,
)
from sqlalchemy.sql import func, text
from datetime import datetime
from util.db import DB


class QueryCountByIp(Base):
    __tablename__ = "QUERY_COUNT_BY_IP"
    __table_args__ = Base.get_default_schema()

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    ip: Mapped[str] = mapped_column(String)
    query_count: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    def retrieve_query_count(ip: str, today_date: str):
        with DB.engine.connect() as conn:
            stmt = select(QueryCountByIp).where(
                QueryCountByIp.ip == ip,
                QueryCountByIp.created_at == today_date,
            )
            return conn.execute(stmt).first()

    def init_query_count(ip: str):
        with DB.engine.connect() as conn:
            stmt = insert(QueryCountByIp).values(ip=ip, query_count=1)
            conn.execute(stmt)
            conn.commit()

    def update_query_count(ip: str, today_date: str, query_count: int):
        with DB.engine.connect() as conn:
            stmt = (
                update(QueryCountByIp)
                .where(
                    QueryCountByIp.ip == ip,
                    QueryCountByIp.created_at == today_date,
                )
                .values(query_count=query_count)
            )
            conn.execute(stmt)
            conn.commit()

    def list_expired_ip(days_expired: int):
        with DB.engine.connect() as conn:
            stmt = (
                select(QueryCountByIp.ip)
                .distinct()
                .where(
                    func.hour(func.timediff(func.now(), QueryCountByIp.updated_at))
                    > days_expired * 24
                )
            )
            return conn.execute(stmt).all()
