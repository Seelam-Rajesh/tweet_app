import re
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from tweets import tweet_function
from IPython.display import HTML

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'

db = SQLAlchemy(app)

html_resp = ""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)

    def __init__(self, name, username):
        self.name = name
        self.username = username
        
@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        my_data = session.get("my_data", None)
        tweets_df = pd.DataFrame(my_data, columns = ['Date', 'Tweet ID', "Tweets"])
        message = tweets_df.to_html()
        print(my_data)
        print(tweets_df)
        message = HTML(tweets_df.to_html())
        #message = [tweets_df.to_html()]
        return render_template('home.html', message = message )
    else:
        return render_template('index.html', message="Hello!")
    
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], name=request.form['name']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        #data = User.query.filter_by(username=u).first()
        if username != "":
            message = tweet_function.tweet(username)
            session['logged_in'] = True
            session["my_data"] = message
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run()
