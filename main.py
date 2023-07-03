from flask import Flask, render_template, request, redirect, url_for,session
import pymysql
app = Flask(__name__)
app.secret_key='your_secret_key'
@app.route('/')
def index():
    if 'id' in session:
        return render_template("index.html",loggedid=session['id'])
    return render_template('index.html',loggedid=-1)

@app.route('/login/',methods=['GET', 'POST'])
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

@app.route('/signup/')
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        db = pymysql.connect(host="localhost", user="root", password="Jtnic027", database="jobdb")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE name=%s",(username))
        namelist=cursor.fetchall()  ##判断用户名
        cursor.execute("SELECT * FROM users WHERE email=%s",(email))
        emaillist=cursor.fetchall() ##判断邮箱
        if(len(namelist) or len(emaillist)):
            error="用户名或邮箱已经注册"
            return render_template('signup.html',error=error)
        elif(password2!=password):
            error="两次密码不一致"
            return render_template('signup.html', error=error)
        else:
            sql="""INSERT INTO users
            (name,pass,email)
            VALUES(%s,%s,%s)"""
            try:
                cursor.execute(sql,(username,password,email))
                db.commit()
            except:
                db.rollback()
        db.close()
    return render_template('signup.html')

@app.route('/forget/')
def forget():
    return render_template('forget.html')

@app.route('/rank')
def rank():
    return render_template('rank.html')

@app.route('/money')
def money():
    return render_template('money.html')

@app.route('/personal/<id>')
def personal(id):
    if 'id' in session:
        return render_template('personal.html', id=id, loggedid=session['id'])
    return render_template('personal.html',id=id,loggedid=-1)

@app.route('/movieinfo/<movieid>')
def movieinfo(movieid):
    return render_template('movieinfo.html',movieid=movieid)

@app.route('/favorite/<id>')
def favorite(id):
    return render_template('favorite.html',id=id)


if __name__ == '__main__':
    app.run('0.0.0.0',debug = True)
