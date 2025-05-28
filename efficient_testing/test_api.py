import uuid
from typing import Callable

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from efficient_testing.dependency import get_todo_repository, get_uuid_provider
from efficient_testing.main import app
from efficient_testing.models import ToDo
from efficient_testing.repository import TodoRepository
from efficient_testing.uuid_provider import FixedUUIDProvider


@pytest.fixture
def create_api_client() -> Callable[..., TestClient]:
    def _create_api_client(**kwargs) -> TestClient:
        dependency_overrides = kwargs.get("dependency_overrides", {})
        app.dependency_overrides.update(dependency_overrides)
        return TestClient(app)

    app.dependency_overrides.clear()

    yield _create_api_client


def test_create_todo(
    create_api_client: Callable[..., TestClient], create_todo_repository: Callable[..., TodoRepository], snapshot
) -> None:
    id_ = uuid.UUID("d2ab1f78-f1ba-44da-9c82-beed46284466")
    todo_repository = create_todo_repository()
    client = create_api_client(
        dependency_overrides={
            get_uuid_provider: lambda: FixedUUIDProvider(id_),
            get_todo_repository: lambda: todo_repository,
        }
    )
    response = client.post(
        "/todos/",
        json={"title": "Test Todo", "description": "This is a test todo", "completed": False},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == snapshot


def test_read_all_todos(
    create_api_client: Callable[..., TestClient],
    create_todo: Callable[..., ToDo],
    create_todo_repository: Callable[..., TodoRepository],
    snapshot,
) -> None:
    todo_repository = create_todo_repository(
        todos=[
            create_todo(
                id="d2ab1f78-f1ba-44da-9c82-beed46284466",
                title="Test Todo 1",
                description="This is the first test todo",
                completed=False,
            ),
            create_todo(
                id="b3ab1f78-f1ba-44da-9c82-beed46284467",
                title="Test Todo 2",
                description="This is the second test todo",
                completed=True,
            ),
        ]
    )
    client = create_api_client(
        dependency_overrides={
            get_todo_repository: lambda: todo_repository,
        }
    )
    response = client.get("/todos/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot


def test_read_todo(
    create_api_client: Callable[..., TestClient],
    create_todo: Callable[..., ToDo],
    create_todo_repository: Callable[..., TodoRepository],
    snapshot,
) -> None:
    todo = create_todo(
        id="d2ab1f78-f1ba-44da-9c82-beed46284466", title="Test Todo", description="This is a test todo", completed=False
    )
    todo_repository = create_todo_repository(
        todos=[
            todo,
        ]
    )
    client = create_api_client(
        dependency_overrides={
            get_todo_repository: lambda: todo_repository,
        }
    )
    response = client.get(f"/todos/{todo.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot


def test_update_todo(
    create_api_client: Callable[..., TestClient],
    create_todo: Callable[..., ToDo],
    create_todo_repository: Callable[..., TodoRepository],
    snapshot,
) -> None:
    todo = create_todo(
        id="d2ab1f78-f1ba-44da-9c82-beed46284466", title="Test Todo", description="This is a test todo", completed=False
    )
    todo_repository = create_todo_repository(
        todos=[
            todo,
        ]
    )
    client = create_api_client(
        dependency_overrides={
            get_todo_repository: lambda: todo_repository,
        }
    )

    response = client.put(
        f"/todos/{todo.id}",
        json={"title": "Updated Todo", "description": "This is an updated test todo", "completed": True},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot


def test_delete_todo(
    create_api_client: Callable[..., TestClient],
    create_todo: Callable[..., ToDo],
    create_todo_repository: Callable[..., TodoRepository],
) -> None:
    todo = create_todo(
        id="d2ab1f78-f1ba-44da-9c82-beed46284466", title="Test Todo", description="This is a test todo", completed=False
    )
    todo_repository = create_todo_repository(
        todos=[
            todo,
        ]
    )
    client = create_api_client(
        dependency_overrides={
            get_todo_repository: lambda: todo_repository,
        }
    )

    response = client.delete(f"/todos/{todo.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
