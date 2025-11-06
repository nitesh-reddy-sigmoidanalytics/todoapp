from fastapi import Depends,APIRouter,HTTPException,status
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models
from models import Todos ,User
from pydantic import BaseModel ,Field
from routers.auth import get_current_user
from passlib.context import  CryptContext



router=APIRouter(
  prefix="/user_details",
  tags=["user_details"]
)

# models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

class Changepassword(BaseModel):
  password:str


def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependecny=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get("/")
async def user_details(user:user_dependency,db:db_dependecny):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
  user=db.query(User).filter(User.id==user["id"]).first()
  return user

@router.post("/change_password")
async def change_password(user:user_dependency,db:db_dependecny,change_password:Changepassword):
  user_details_model=db.query(User).filter(User.id==user["id"]).first()
  user_details_model.hashed_password=bcrypt_context.hash(change_password.password)
  db.add(user_details_model)
  db.commit()

