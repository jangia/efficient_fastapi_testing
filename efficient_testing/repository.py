from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from .models import ToDo


class TodoRepository(ABC):
    @abstractmethod
    def list_todos(self) -> list[ToDo]:
        raise NotImplementedError

    @abstractmethod
    def get_todo(self, todo_id: str) -> ToDo:
        raise NotImplementedError

    @abstractmethod
    def add_todo(self, todo: ToDo) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_todo(self, todo_id: str) -> None:
        raise NotImplementedError


class TodoRepositoryInMemory(TodoRepository):
    def __init__(self):
        self._todos = {}

    def list_todos(self) -> list[ToDo]:
        return list(self._todos.values())

    def get_todo(self, todo_id: str) -> ToDo:
        return self._todos[todo_id]

    def add_todo(self, todo: ToDo) -> None:
        self._todos[todo.id] = todo

    def delete_todo(self, todo_id: str) -> None:
        del self._todos[todo_id]


class TodoRepositorySQLite(TodoRepository):
    def __init__(self, session: Session):
        self._session = session

    def list_todos(self) -> list[ToDo]:
        return self._session.query(ToDo).all()

    def get_todo(self, todo_id: str) -> ToDo:
        return self._session.query(ToDo).filter(ToDo.id == todo_id).one()

    def add_todo(self, todo: ToDo) -> None:
        self._session.add(todo)
        self._session.commit()

    def delete_todo(self, todo_id: str) -> None:
        todo = self.get_todo(todo_id)
        self._session.delete(todo)
        self._session.commit()
