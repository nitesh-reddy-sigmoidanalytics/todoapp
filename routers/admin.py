from fastapi import Depends,APIRouter,HTTPException,status
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models
from models import Todos
from pydantic import BaseModel ,Field
from routers.auth import get_current_user



router=APIRouter(
  prefix="/admin",
  tags=["admin"]
)

# models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)



class TodoRequest(BaseModel):
  title: str=Field(min_length=3)
  desc: str  = Field(min_length=1,max_length=100)
  rating: int = Field(gt=1,lt=6)
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
async def read_all(user:user_dependency,db:db_dependecny):
  if user is  None or user["user_role"]!="admin":
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  return db.query(Todos).all()
