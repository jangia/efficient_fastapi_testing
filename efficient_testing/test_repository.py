from abc import ABC, abstractmethod
from typing import Callable

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from efficient_testing.database import Base
from efficient_testing.models import ToDo
from efficient_testing.repository import TodoRepository, TodoRepositoryInMemory, TodoRepositorySQLite


class RepositoryContract(ABC):
    @pytest.fixture
    @abstractmethod
    def repo(self) -> TodoRepository:
        raise NotImplementedError

    def test_added_todo_fetched(self, repo: TodoRepository, create_todo: Callable[..., ToDo]):
        todo = create_todo()

        repo.add_todo(todo)

        assert repo.get_todo(todo.id) == todo
        assert repo.list_todos()[0] == todo

    def test_todo_removed(self, repo: TodoRepository, create_todo: Callable[..., ToDo]):
        todo = create_todo()
        repo.add_todo(todo)

        repo.delete_todo(todo.id)

        with pytest.raises(Exception):
            repo.get_todo(todo.id)


class TestInMemoryRepository(RepositoryContract):
    @pytest.fixture
    def repo(self) -> TodoRepositoryInMemory:
        return TodoRepositoryInMemory()


class TestSQLiteRepository(RepositoryContract):
    @pytest.fixture
    def session(self):
        engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(engine)
        s = sessionmaker(bind=engine)
        session = s()
        yield session
        session.close()
        Base.metadata.drop_all(engine)

    @pytest.fixture
    def repo(self, session) -> TodoRepositorySQLite:
        return TodoRepositorySQLite(session)
