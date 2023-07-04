from dbCon import DB_URI
from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# 创建标签实体类
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))

    movies = relationship("Movie", secondary=movie_tag_table, back_populates="tags")
