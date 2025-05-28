import uuid

from sqlalchemy import Boolean, Column, String

from .database import Base


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    completed = Column(Boolean, default=False)
    # priority = Column(Integer, nullable=False)
