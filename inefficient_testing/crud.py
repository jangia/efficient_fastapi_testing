from sqlalchemy.orm import Session

from . import models, schemas


def get_todos(db: Session):
    return db.query(models.ToDo).all()


def get_todo(db: Session, todo_id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.ToDoUpdate):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True
