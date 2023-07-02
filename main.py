from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('personal.html',id=id)

@app.route('/movieinfo/<id>')
def movieinfo(id):
    return render_template('movieinfo.html',id=id)

@app.route('/favorite/<id>')
def favorite(id):
    return render_template('favorite.html',id=id)


if __name__ == '__main__':
    app.run('0.0.0.0',debug = True)
