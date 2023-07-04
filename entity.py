from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from dbCon import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import relationship

engine = create_engine(DB_URI,echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# 创建一个用户的类
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    password=Column(String(255))
    email = Column(String(255))
    comm = relationship('Comments', back_populates='user')

class Movie(Base):
    # 定义表名为movieinfo
    __tablename__ = 'movieinfo'
    # 将id设置为主键，并且默认是自增长的
    id = Column(Integer,primary_key=True)
    # name字段，字符类型，最大的长度是50个字符
    title = Column(String(255))
    img = Column(String(255))
    director = Column(String(255))
    actors = Column(String(255))
    style1 = Column(String(255))
    style2 = Column(String(255))
    style3 = Column(String(255))
    country = Column(String(255))
    language = Column(String(255))
    release_date = Column(Integer)
    writer = Column(String(255))
    running_time = Column(Integer)
    score = Column(Integer)
    Introduction = Column(String(1000))
    comm = relationship('Comments', back_populates='movie')

class Comments(Base):
    # 定义表名movie_comment
    __tablename__ = 'movie_comment'
    # 将id设置为主键，并且默认是自增长的
    id = Column(Integer,primary_key=True)
    # name字段，字符类型，最大的长度是50个字符
    user_id = Column(Integer,ForeignKey('user.id'))
    score = Column(Float)
    createtime = Column(DateTime)
    comments = Column(String(2000))
    movie_id = Column(Integer,ForeignKey('movieinfo.id'))
    user = relationship('User',back_populates="comm")
    movie = relationship('Movie',back_populates="comm")

class FavoriteList(Base):
    __tablename__ = 'favorite_lists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    movie_id = Column(Integer, ForeignKey('movieinfo.id'))
    created_at = Column(DateTime, default=datetime.now())

