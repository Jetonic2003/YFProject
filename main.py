from flask import Flask, render_template, request, redirect, url_for
import pymysql
app = Flask(__name__)

loggedid=-1
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        username=request.form['nm']
        password=request.form['pw']
        db=pymysql.connect(host="localhost",user="root",password="Jtnic027",database="jobdb")
        cursor=db.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s AND pass=%s",(username,password))
        user=cursor.fetchone()
        if user:
            # 用户登录成功
            return redirect(url_for('index'))
        else:
            error = '无效的用户名或密码，请重试。'
            return render_template('login.html', error=error)

        cur.close()
    return render_template('login.html')

@app.route('/signup/')
def signup():
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
    global loggedid
    return render_template('personal.html',id=id,loggedid=loggedid)

@app.route('/movieinfo/<movieid>')
def movieinfo(movieid):
    return render_template('movieinfo.html',movieid=movieid)

@app.route('/favorite/<id>')
def favorite(id):
    return render_template('favorite.html',id=id)


if __name__ == '__main__':
    app.run('0.0.0.0',debug = True)
