from dbCon import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from entity import FavoriteList

engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


    # 在收藏夹中添加电影
def add_movie_to_favorite(user_id, movie_id):
    favorite = session.query(FavoriteList).filter_by(user_id=user_id, movie_id=movie_id).first()
    if favorite:
        return favorite
    else:
        favorite = FavoriteList(user_id=user_id, movie_id=movie_id)
        session.add(favorite)
        session.commit()
        return favorite

    # 从收藏夹中移除电影
def remove_movie_from_favorite(id):
    favorite = session.query(FavoriteList).filter_by(id=id).first()
    if favorite:
        session.delete(favorite)
        session.commit()
    return favorite

    # 根据 ID 获取收藏夹记录
def get_favorite_by_id(id):
    favorite = session.query(FavoriteList).filter_by(id=id).first()
    return favorite

    # 根据用户 ID 获取该用户的所有收藏记录
def get_favorites_by_user_id(user_id):
    favorites = session.query(FavoriteList).filter_by(user_id=user_id).all()
    return favorites

    # 更新收藏夹记录
def update_favorite( id, user_id=None, movie_id=None):
    favorite = get_favorite_by_id(id)
    if favorite:
        if user_id:
            favorite.user_id = user_id
        if movie_id:
            favorite.movie_id = movie_id
        session.commit()
    return favorite
