from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL= f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
#sqlite:///./tododb
# postgress ="postgresql://postgres:1234!@127.0.0.1/todoApplicationDatabase"
# mysql =""mysql+pymysql://root:Test1234!@127.0.0.1/todoApplicationDatabase""

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

