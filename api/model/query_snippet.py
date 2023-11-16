from model.common import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, BigInteger, DateTime, UniqueConstraint, select
from sqlalchemy.sql import func, text
from datetime import datetime
from util.db import DB


class QuerySnippet(Base):
    __tablename__ = "QUERY_SNIPPET"
    __table_args__ = (UniqueConstraint("common_code"), Base.get_default_schema())

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    common_code: Mapped[str] = mapped_column(String)
    snippet: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    def retrieve_table_query_snippet():
        with DB.engine.connect() as conn:
            stmt = select(QuerySnippet).where(
                QuerySnippet.common_code == "table-query-snippet"
            )
            return conn.execute(stmt).first()

    def retrieve_constraint_query_snippet():
        with DB.engine.connect() as conn:
            stmt = select(QuerySnippet).where(
                QuerySnippet.common_code == "constraint-query-snippet"
            )
            return conn.execute(stmt).first()
