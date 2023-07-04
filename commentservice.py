# 引入相关模块和库
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity import User,Comments
from dbCon import DB_URI

class CommentService:
    # 初始化数据库连接
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # 添加新评论
    def add_comment(self, user_id, movie_id, content, score):
        comment = Comment(user_id=user_id, movie_id=movie_id, content=content, score=score, create_time=datetime.now())
        self.session.add(comment)
        self.session.commit()
        return comment.id

    # 获取某一电影的所有评论
    def get_comments_by_movie_id(self, movie_id):
        comments = self.session.query(Comment).filter_by(movie_id=movie_id).all()
        return comments

    # 获取某一用户发布的所有评论
    def get_comments_by_user_id(self, user_id):
        comments = self.session.query(Comment).filter_by(user_id=user_id).all()
        return comments

    # 获取某一评论的详细信息
    def get_comment_by_id(self, comment_id):
        comment = self.session.query(Comment).filter_by(id=comment_id).first()
        return comment




