from model.common import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, BigInteger, DateTime, UniqueConstraint
from sqlalchemy.sql import func, text
from datetime import datetime


class CommonCode(Base):
    __tablename__ = "COMMON_CODE"
    __table_args__ = (UniqueConstraint("code"), Base.get_default_schema())

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
