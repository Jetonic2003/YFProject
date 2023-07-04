import pandas as pd
from flask import Flask, render_template, request, redirect, url_for,session
import pymysql
import requests
import movieservice,commentservice,entity,userservice,favoriteservice

app = Flask(__name__)
app.secret_key='your_secret_key'

@app.route('/')
def index():
    newmovies=movieservice.getnmovie(4)
    if 'id' in session:
        return render_template("index.html",loggedid=session['id'],**{'movies':newmovies})
    return render_template('index.html',loggedid=-1,**{'movies':newmovies})

@app.route('/login/',methods=['GET', 'POST'])   # 登录
def login():
    if request.method=="POST":
        username=request.form['nm']
        password=request.form['pw']
        db=pymysql.connect(host="localhost",user="root",password="Jtnic027",database="jobdb")
        cursor=db.cursor()
        cursor.execute("SELECT * FROM user WHERE email=%s AND password=%s",(username,password))
        user=cursor.fetchone()
        if user:
            # 用户登录成功
            session['id']=user[0]
            session['username']=user[1]
            return redirect(url_for('index'))
        else:
            error = '无效的用户名或密码，请重试。'
            return render_template('login.html', error=error)

        cur.close()
    return render_template('login.html')

@app.route('/signup/',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE name=%s", username)
        namelist=cursor.fetchone()  ##判断用户名
        cursor.execute("SELECT * FROM user WHERE email=%s", email)
        emaillist=cursor.fetchone() ##判断邮箱
        if(namelist or emaillist):
            error="用户名或邮箱已经注册"
            return render_template('signup.html',error=error)
        elif(password2!=password):
            error="两次密码不一致"
            return render_template('signup.html', error=error)
        else:
            sql="INSERT INTO user (name,password,email) VALUES(%s,%s,%s)"
            try:
                cursor.execute(sql,(username,password,email))
                db.commit()
                return redirect(url_for('login'))
            except:
                db.rollback()
                error="数据库操作出错"
                return render_template('signup.html', error=error)
        db.close()
    return render_template('signup.html')

@app.route('/forget/')
def forget():
    return render_template('forget.html')

@app.route('/rank')
def rank():
    movies=movieservice.getTopnMovie(10)
    if 'id' in session:
        return render_template('rank.html', loggedid=session['id'],**{'movies':movies})
    return render_template('rank.html',loggedid=-1,**{'movies':movies})

@app.route('/personal/')
def personal():
    if 'id' in session:
        db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM user WHERE id=%s", session['id'])
        nickname=cursor.fetchone()[0]
        return render_template('personal.html', loggedid=session['id'],nickname=nickname)
    return "请先登录/注册"

@app.route('/changename/',methods=["POST","GET"])
def changename():
    if 'id' in session:
        if request.method=="POST":
            nickname = request.form.get('nickname')
            db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE name=%s", nickname)
            dump=cursor.fetchone()
            if(dump):
                db.close()
            else:
                cursor.execute("UPDATE user SET name=%s WHERE id=%s",(nickname,session['id']))
                db.commit()
                db.close()
        return redirect(url_for("personal"))
    return "请先登录/注册"

@app.route('/changepass/',methods=["POST","GET"])
def changepass():
    if 'id' in session:
        if request.method=="POST":
            oldpassword = request.form.get('oldpw')
            password = request.form.get('pw')
            password2 = request.form.get('pw2')
            if(password2!=password):
                error="两次密码不一致"
                return render_template('changepass.html',error=error)
            db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
            cursor = db.cursor()
            cursor.execute("SELECT password FROM user WHERE id=%s", session['id'])
            nowpassword = cursor.fetchone()
            if(nowpassword[0]!=oldpassword):
                error = "旧密码输入错误"
                db.close()
                return render_template('changepass.html', error=error)
            try:
                cursor.execute("UPDATE user SET password=%s WHERE id=%s",(password, session['id']))
                db.commit()
                db.close()
                session.clear()
                return "密码已修改，请重新登录"
            except:
                db.rollback()
                error="数据库操作失败，请重试"
                db.close()
                return render_template('changepass.html', error=error)
        return render_template('changepass.html')
    else:
        return "当前未登录，请登陆后操作"

@app.route('/movieinfo/<movieid>')
def movieinfo(movieid):
    movie=movieservice.getMovieByID(movieid)
    if 'id' in session:
        return render_template('movieinfo.html', movie=movie, loggedid=session['id'])
    return render_template('movieinfo.html',movie=movie,loggedid=-1)

@app.route('/favorite/')
def favorite():
    db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM user WHERE id=%s", session['id'])
    username=cursor.fetchone()[0]
    db.close()
    favorites=favoriteservice.get_favorites_by_user_id(session['id'])
    fmovie_info=[]
    for favorite in favorites:
        fmovie_id=favorite.movie_id
        one_info=movieservice.getMovieByID(fmovie_id)
        one_favorite={}
        one_favorite['img']=one_info.img
        one_favorite['title']=one_info.title
        fmovie_info.append(one_favorite)
    return render_template('favorite.html',username=username,loggedid=session['id'],**{'favorites':fmovie_info})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0',debug = True)
