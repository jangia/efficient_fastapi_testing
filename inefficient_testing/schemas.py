from typing import Optional

from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ToDoOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    model_config = ConfigDict(from_attributes=True)
