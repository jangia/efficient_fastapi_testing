import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from . import models
from .database import Base
from .main import app, get_db
from .schemas import ToDoRead

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency override for FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Set up schema before each test
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_create_todo():
    res = client.post("/todos/", json={"title": "Test", "description": "Something"})
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Test"
    assert "id" in data


def test_get_todo(db_session):
    todo = models.ToDo(title="Prefilled", description="Seeded todo")
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    res = client.get(f"/todos/{todo.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == todo.id
    assert data["title"] == "Prefilled"


def test_update_todo(db_session):
    todo = models.ToDo(title="Prefilled", description="Seeded todo")
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    res = client.put(f"/todos/{todo.id}", json={"completed": True})
    assert res.status_code == 200
    assert res.json()["completed"] is True


def test_delete_todo(db_session):
    todo = models.ToDo(title="Prefilled", description="Seeded todo")
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    del_res = client.delete(f"/todos/{todo.id}")
    assert del_res.status_code == 200


def test_list_todos(db_session):
    todo = models.ToDo(title="Task 1", description="Seeded todo")
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    res = client.get("/todos/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1

    assert all(ToDoRead(**todo) for todo in data)
