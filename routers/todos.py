from fastapi import Depends,APIRouter,HTTPException,status
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models
from models import Todos
from pydantic import BaseModel ,Field
from routers.auth import get_current_user


router=APIRouter()

# models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)



class TodoRequest(BaseModel):
  title: str=Field(min_length=3)
  description: str  = Field(min_length=1,max_length=100)
  priority: int = Field(gt=1,lt=6)
  complete: bool


def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependecny=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/")
def read_all(user:user_dependency,db: db_dependecny):
  return db.query(Todos).filter(Todos.owner_id==user["id"]).all()

@router.get("/todos/{todo_id}")
def get_by_id(user:user_dependency,todo_id:int , db: db_dependecny):
  todo_model=db.query(Todos).filter(Todos.id == todo_id ).filter(Todos.owner_id==user["id"]).first()
  return todo_model


@router.post("/create_todo/")
def create_todo(user:user_dependency,db: db_dependecny,todo_request:TodoRequest):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="authentication failed")
  todo_model=Todos(**todo_request.model_dump(),owner_id=user["id"])
  db.add(todo_model)
  db.commit()

@router.put("/update_todo")
def update_todo(user:user_dependency,db:db_dependecny,todo_request:TodoRequest,todo_id:int):
  todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user["id"]).first()
  if not todo_model:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not fond")


  todo_model.title=todo_request.title
  todo_model.description=todo_request.description
  todo_model.priority=todo_request.priority
  todo_model.complete=todo_request.complete

  db.add(todo_model)
  db.commit()

@router.delete("/delete_todo")
def delete_todo(user:user_dependency,db:db_dependecny,todo_id:int):
  todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
  if not todo_model:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user["id"]).delete()
  db.commit()

