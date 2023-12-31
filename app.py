from flask import Flask, render_template, request, redirect, url_for,session
import movieservice,commentservice,entity,userservice,favoriteservice
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
app = Flask(__name__)
app.secret_key='your_secret_key'
forget_captcha=""

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
        user=userservice.userlogin(username,password)
        if user:
            # 用户登录成功
            session['id']=user.id
            session['username']=user.name
            return redirect(url_for('index'))
        else:
            error = '无效的用户名或密码，请重试。'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup/',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if(password!=password2):
            error="两次密码不一致"
            return render_template('signup.html', error=error)
        elif(userservice.get_user_by_email(email) or userservice.get_user_by_name(username)):
            error="用户名或邮箱已注册"
            return render_template('signup.html',error=error)
        else:
            userservice.create_user(username,password,email)
            return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/forget/',methods=['GET', 'POST'])
def forget():
    global forget_captcha
    forget_captcha=""
    if 'id' in session:
        return "请退出账号再进行相关操作"
    if request.method=="POST":
        emailname=request.form.get('email')
        if not userservice.get_user_by_email(emailname):
            error="查无此人！请重新输入邮箱。"
            return render_template("forget.html",error=error)
        session['email']=emailname
        # 创建邮件主体对象
        email = MIMEMultipart()
        # 设置发件人、收件人和主题
        email['From'] = '15327327862@163.com'
        email['To'] = emailname
        email['Subject'] = Header('发送验证码', 'utf-8')
        for i in range(4):
            forget_captcha+=chr(random.randint(48,57))
        # 添加邮件正文内容
        content = forget_captcha+"这是您的验证码"
        email.attach(MIMEText(content, 'plain', 'utf-8'))
        # 创建SMTP_SSL对象（连接邮件服务器）
        smtp_obj = smtplib.SMTP_SSL('smtp.163.com', 465)
        # 通过用户名和授权码进行登录
        smtp_obj.login('15327327862@163.com', 'UJSNRLCSKVMDHIQR')
        # 发送邮件（发件人、收件人、邮件内容（字符串））
        smtp_obj.sendmail(
            '15327327862@163.com',
            emailname,
            email.as_string()
        )
        return redirect(url_for('forget_cap'))
    return render_template('forget.html')

@app.route('/forget_cap/',methods=['GET', 'POST'])
def forget_cap():
    global forget_captcha
    if request.method=="POST":
        captcha=request.form.get('captcha')
        if(captcha!=forget_captcha):
            error="验证码错误，请重新输入"
            return render_template('forget_captcha.html',error=error)
        else:
            forget_captcha=""   # 清空验证码
            return redirect(url_for('forget_changepass'))
    return render_template('forget_captcha.html')

@app.route('/forget_changepass/',methods=['GET', 'POST'])
def forget_changepass():
    if request.method=="POST":
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if(password!=password2):
            error="两次密码不一致，请检查"
            return render_template('forget_changepass.html',error=error)
        else:
            user=userservice.get_user_by_email(session['email'])
            userservice.update_user(user.id,None,password)
            session.clear()
            return "恭喜！您的密码已经成功找回，请重新登录！"
    return render_template('forget_changepass.html')

@app.route('/rank')
def rank():
    movies=movieservice.getTopnMovie(10)
    if 'id' in session:
        return render_template('rank.html', loggedid=session['id'],**{'movies':movies})
    return render_template('rank.html',loggedid=-1,**{'movies':movies})

@app.route('/personal/')
def personal():
    if 'id' in session:
        user=userservice.get_user_by_id(session['id'])
        nickname=user.name
        return render_template('personal.html', loggedid=session['id'],nickname=nickname)
    return "请先登录/注册"

@app.route('/changename/',methods=["POST","GET"])
def changename():
    if 'id' in session:
        if request.method=="POST":
            nickname = request.form.get('nickname')
            if(not userservice.get_user_by_name(nickname)):
                userservice.update_user(session['id'],nickname)
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
            nowpassword=userservice.get_user_by_id(session['id']).password
            if(nowpassword!=oldpassword):
                error = "旧密码输入错误"
                return render_template('changepass.html', error=error)
            try:
                userservice.update_user(session['id'],None,password)
                session.clear()
                return "密码已修改，请重新登录"
            except:
                error="数据库操作失败，请重试"
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
    username=userservice.get_user_by_id(session['id']).name
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
