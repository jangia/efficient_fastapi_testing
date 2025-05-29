from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status

from . import schemas
from .database import Base, engine
from .dependency import get_todo_repository, get_uuid_provider
from .models import ToDo
from .repository import TodoRepository
from .uuid_provider import UUIDProvider

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/todos/", status_code=status.HTTP_201_CREATED)
def create(
    data: schemas.ToDoCreate,
    uuid_provider: UUIDProvider = Depends(get_uuid_provider),
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> schemas.ToDoRead:
    todo = ToDo(id=uuid_provider.uuid4(), title=data.title, description=data.description, completed=False)
    todo_repository.add_todo(todo)
    return schemas.ToDoRead.model_validate(todo)


@app.get("/todos/")
def read_all(
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> list[schemas.ToDoRead]:
    todos = todo_repository.list_todos()

    return [schemas.ToDoRead.model_validate(todo) for todo in todos]


@app.get("/todos/{todo_id}")
def read(
    todo_id: UUID,
    todo_repository: TodoRepository = Depends(get_todo_repository),
) -> schemas.ToDoRead:
    todo = todo_repository.get_todo(str(todo_id))
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    return schemas.ToDoRead.model_validate(todo)


@app.put("/todos/{todo_id}", response_model=schemas.ToDoRead)
def update(
    data: schemas.ToDoUpdate,
    todo_id: UUID,
    todo_repository: TodoRepository = Depends(get_todo_repository),
):
    todo = todo_repository.get_todo(str(todo_id))
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")

    todo.title = data.title
    todo.description = data.description
    todo.completed = data.completed

    todo_repository.add_todo(todo)
    return schemas.ToDoRead.model_validate(todo)


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(todo_id: UUID, todo_repository: TodoRepository = Depends(get_todo_repository)) -> None:
    todo_repository.delete_todo(str(todo_id))
