import uuid
from typing import Callable

import pytest

from efficient_testing.models import ToDo
from efficient_testing.repository import TodoRepository, TodoRepositoryInMemory


@pytest.fixture
def create_todo() -> Callable[..., ToDo]:
    def _create_todo(**kwargs) -> ToDo:
        return ToDo(
            id=kwargs.get("id", str(uuid.uuid4())),
            title=kwargs.get("title", "Buy milk"),
            description=kwargs.get("description", "From the store"),
            completed=kwargs.get("completed", False),
            # priority=kwargs.get("priority", 1),
        )

    return _create_todo


@pytest.fixture
def create_todo_repository() -> Callable[..., TodoRepository]:
    def _create_todo_repository(**kwargs) -> TodoRepository:
        repository = TodoRepositoryInMemory()
        for todo in kwargs.get("todos", []):
            repository.add_todo(todo)

        return repository

    return _create_todo_repository
