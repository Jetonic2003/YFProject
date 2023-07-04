from sqlalchemy import create_engine
from dbCon import DB_URI
from sqlalchemy.orm import sessionmaker
from moviebase import Movie

#连接数据库
engine = create_engine(DB_URI,echo=True)
#使用model对象添加数据
Session = sessionmaker(bind=engine)
session = Session()
#初始对象的值