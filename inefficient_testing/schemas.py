from typing import Optional

from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ToDoOut(ToDoCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True
