from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from models import User
from passlib.context import  CryptContext
from database import SessionLocal
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from models import User
from jose import jwt,JWTError
from datetime import timedelta,datetime


router=APIRouter(
  prefix="/auth",
  tags=["auth"]
)


SECRET_KEY="2ee80801effe108d859d6cbd46918c2d74a8c7fe2de8f129d01f704412f92cd2" #openssl rand -hex 32
ALGORITHIM="HS256"

#datetime.now(timezone.utc)



bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

outh2_bearer=OAuth2PasswordBearer(tokenUrl='/auth/token')




def authenticate_user(username,password,db):
  user=db.query(User).filter(User.username==username).first()
  if not user:
    return False
  if not bcrypt_context.verify(password,user.hashed_password):
    return False
  return user


def create_access_token(username:str,user_id:int,role:str,expires_delta:timedelta):
  encode={"sub":username,"id":user_id,"role":role}
  expires=datetime.now()+expires_delta
  encode.update({"exp":expires})
  return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHIM)

async def get_current_user(token:Annotated[str,Depends(outh2_bearer)]):
  try:
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHIM])
    username:str=payload.get('sub')
    user_id:int=payload.get('id')
    user_role=payload.get('role')
    if username is None or user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate user")
    return {'username': username, 'id': user_id, 'user_role': user_role}
  except JWTError:
     if username is None or user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate user")





class CreateUserRequest(BaseModel):


  email:str
  username:str
  first_name:str
  last_name:str
  role:str
  password:str
  is_active:bool
  role:str
  phone_number:Optional[str]=None

class Updatenumber(BaseModel):
  phone_number:str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependecny=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]




@router.post("/")
def create(db:db_dependecny,create_user_request:CreateUserRequest):
  user_model=User(
    email=create_user_request.email,
    username=create_user_request.username,
    first_name=create_user_request.first_name,
    last_name=create_user_request.last_name,
    role=create_user_request.role,
    hashed_password=bcrypt_context.hash(create_user_request.password),
    is_active=create_user_request.is_active,
    phone_number=create_user_request.phone_number

  )
  db.add(user_model)
  db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependecny):
  user=authenticate_user(form_data.username,form_data.password,db)
  if not user:
    raise HTTPException(status_code=404,detail="user not found")
  token=create_access_token(user.username,user.id,user.role,timedelta(minutes=50))

  return {"access_token":token,"token_type":"bearer"}

@router.put("/")
async def update_phone_number(db:db_dependecny,req_number:Updatenumber,user:user_dependency):
  user_model=db.query(User).filter(User.id==user["id"]).first()
  if not user_model:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  user_model.phone_number=req_number.phone_number
  db.add(user_model)
  db.commit()

@router.delete("/delete_user")
async def delete_user(db:db_dependecny,user:user_dependency,id:int):
  if user["user_role"]=='admin':
    db.query(User).filter(User.id==id).delete()
    db.commit()
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)






#pip install pysco2-binary
