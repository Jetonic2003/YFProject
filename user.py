from sqlalchemy import Column,Integer,String,DateTime,ForeignKey
from dbCon import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

engine = create_engine(DB_URI,echo=True)
Base = declarative_base(engine)

# 创建一个用户的类
class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    password=Column(String(255))
    email = Column(String(255))