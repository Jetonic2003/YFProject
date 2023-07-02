from flask import Flask, render_template,request

app = Flask(__name__)

loggedid=-1
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
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
