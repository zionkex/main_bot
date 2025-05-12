from datetime import datetime
from sqlalchemy.orm import relationship
from typing import Optional
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,declared_attr

class Base(DeclarativeBase):
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'
    

class Bot(Base):
    name: Mapped[str] = mapped_column(String(50), unique=False)
    nickname: Mapped[str] = mapped_column(String(50), unique=True)
    manual_url: Mapped[str] = mapped_column(String(200))
    type : Mapped[str] = mapped_column(String(50))


class User(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    telegram_name: Mapped[str] = mapped_column(String, nullable=False)
    telegram_username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    join_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_activity: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    order_count: Mapped[int] = mapped_column(default=0)

    type: Mapped[str] = mapped_column(String(50), nullable=False)

    worker_links = relationship(
        "Workers_Mamont",
        foreign_keys="[Workers_Mamont.worker_id]",
        back_populates="worker",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    mamonts_links = relationship(
        "Workers_Mamont",
        foreign_keys="[Workers_Mamont.mamont_id]",
        back_populates="mamont",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }

    def get_mamonts(self):
        return [link.mamont for link in self.worker_links]

    def get_workers(self):
        return [link.worker for link in self.mamonts_links]


class Worker(User):

    __abstract__ = True

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "worker",
    }


class Mamont(User):
    __abstract__ = True

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "mamont",
    }