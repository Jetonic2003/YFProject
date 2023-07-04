from dbCon import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from entity import User

engine = create_engine(DB_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def create_user( name, password,email):
    user = User(name=name, password=password,email=email)
    session.add(user)
    session.commit()
    return user

def get_user_by_id( id):
    user = session.query(User).filter_by(id=id).first()
    return user

def get_user_by_name(name):
    user = session.query(User).filter_by(name=name).first()
    return user

def get_user_by_email(email):
    user = session.query(User).filter_by(email=email).first()
    return user

def userlogin(email, password):
    user = session.query(User).order_by(User.id).filter_by(email=email,password=password).one_or_none()
    if user!=None:
        return user
    else:
        return 0


def update_user( id, name=None, password=None):
    user = get_user_by_id(id)
    if user:
        if name:
            user.name = name
        if password:
            user.password = password
        session.commit()
    return user

def delete_user( id):
    user = get_user_by_id(id)
    if user:
        session.delete(user)
        session.commit()
    return user

