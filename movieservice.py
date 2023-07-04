from sqlalchemy import create_engine,func
from dbCon import DB_URI
from entity import Comments,Movie,User
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URI,echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#获取全部电影
def getAllmovie():
    movies =session.query(Movie).order_by(-Movie.release_date)
    return movies

#获取前n部电影
def getnmovie(n):
    movies =session.query(Movie).order_by(-Movie.release_date).limit(n)
    return movies

#根据电影名获取电影
def getMovieBytitle(stitle):
    movies =session.query(Movie).filter_by(title=stitle)
    return movies

#获取评分前n的电影
def getTopnMovie(n):
    movies =session.query(Movie).order_by(-Movie.score).limit(n)
    return movies

#获取评分前n的电影，根据电影类型,参数类型名称
def getTopnMovieBytype(stype,n):
    movies =session.query(Movie).order_by(-Movie.score).filter_by(type=stype).limit(n)
    return movies

#获取导演的全部电影
def getMovieBydirector(sdirector):
    movies =session.query(Movie).filter_by(director=sdirector).all()
    return movies

#获取演员的全部电影
def getMovieByactor(sacotor):
    movies =session.query(Movie).filter(Movie.actors.like('%sactor%')).all()
    return movies

#获取指定国家的全部电影
def getMovieBycountry(scountry):
    movies =session.query(Movie).filter_by(country=scountry).all()
    return movies

#获取指定语言的全部电影
def getMovieBylanguage(slanguage):
    movies =session.query(Movie).filter_by(language=slanguage).all()
    return movies

#获取大于等于指定评分的全部电影
def getMovieByscore(sscore):
    movies =session.query(Movie).filter_by(Movie.score>=sscore).all()
    return movies

#获取类型的全部电影,参数类型名称
def getMovieBytype(stype):
    movies =session.query(Movie).filter_by(type=stype).all()
    return movies

#根据ID获取电影详情
def getMovieByID(sid):
    movies =session.query(Movie).filter_by(id=sid)
    return movies

#更新电影评分，参数电影id,成功返回电影id，失败返回0
def updateMoviescore(movie_id):
    #获取平均分
    result = session.query(func.avg(Comments.score)).filter_by(movieid=movie_id)
    if result[0][0] != None:
        #获取电影信息
        movie = getMovieByID(movie_id)
        #更新新的电影评分
        movie[0].score = int(result[0][0])
        #更新数据库电影表数据
        session.add(movie[0])
        #提交更新到数据库
        session.commit()
        return movie[0].id
    else:
        return '0'

