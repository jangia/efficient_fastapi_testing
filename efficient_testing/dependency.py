from efficient_testing.database import SessionLocal
from efficient_testing.repository import TodoRepository, TodoRepositorySQLite
from efficient_testing.uuid_provider import SystemUUIDProvider, UUIDProvider


def get_uuid_provider() -> UUIDProvider:
    return SystemUUIDProvider()


def get_todo_repository() -> TodoRepository:
    return TodoRepositorySQLite(session=SessionLocal())
