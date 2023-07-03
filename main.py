from flask import Flask, render_template, request, redirect, url_for,session
import pymysql
app = Flask(__name__)
app.secret_key='your_secret_key'
@app.route('/')
def index():    # 首页
    if 'id' in session:
        return render_template("index.html",loggedid=session['id'])
    return render_template('index.html',loggedid=-1)

@app.route('/login/',methods=['GET', 'POST'])   # 登录
def login():
    global loggedid
    if request.method=="POST":
        username=request.form['nm']
        password=request.form['pw']
        db=pymysql.connect(host="localhost",user="root",password="Jtnic027",database="jobdb")
        cursor=db.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s AND pass=%s",(username,password))
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
        cursor.execute("SELECT * FROM users WHERE name=%s", username)
        namelist=cursor.fetchone()  ##判断用户名
        cursor.execute("SELECT * FROM users WHERE email=%s", email)
        emaillist=cursor.fetchone() ##判断邮箱
        if(namelist or emaillist):
            error="用户名或邮箱已经注册"
            return render_template('signup.html',error=error)
        elif(password2!=password):
            error="两次密码不一致"
            return render_template('signup.html', error=error)
        else:
            sql="INSERT INTO users (name,pass,email) VALUES(%s,%s,%s)"
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
    if 'id' in session:
        return render_template('rank.html', loggedid=session['id'])
    return render_template('rank.html',loggedid=-1)

@app.route('/money')
def money():
    if 'id' in session:
        return render_template('movieinfo.html', loggedid=session['id'])
    return render_template('money.html',loggedid=-1)

@app.route('/personal/')
def personal():
    if 'id' in session:
        db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM users WHERE id=%s", session['id'])
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
            cursor.execute("SELECT * FROM users WHERE name=%s", name)
            dump=cursor.fetchone()
            if(dump):
                db.close()  # 重复，不予修改
        return render_template('personal.html', loggedid=session['id'],nickname=nickname)
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
            cursor.execute("SELECT pass FROM users WHERE id=%s", session['id'])
            nowpassword = cursor.fetchone()
            if(nowpassword[0]!=oldpassword):
                error = "旧密码输入错误"
                db.close()
                return render_template('changepass.html', error=error)
            try:
                cursor.execute("UPDATE users SET pass=%s WHERE id=%s",(password, session['id']))
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
    if 'id' in session:
        return render_template('movieinfo.html', movieid=id, loggedid=session['id'])
    return render_template('movieinfo.html',movieid=id,loggedid=-1)

@app.route('/favorite/<id>')
def favorite(id):
    db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
    cursor = db.cursor()
    cursor.execute("SELECT name FROM users WHERE id=%s", id)
    username=cursor.fetchone()[0]
    return render_template('favorite.html',username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0',debug = True)
