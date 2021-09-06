import re
import sqlite3
import pandas as pd
from IPython.display import HTML
from tweets import tweet_function
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask import Flask, render_template, request, redirect, url_for, session
# Initializing flask app and database
app = Flask(__name__)
engine = create_engine('sqlite:///twitter.db', echo=False)
cron = APScheduler()
        
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form :
        username = request.form['username']
        session["logged_in"] = True
        data = tweet_function.tweet(username)
        tweet_list = [[i.user.screen_name, i.created_at.strftime("%d/%m/%Y"), i.created_at.strftime("%H:%M:%S"), i.id, i.text] for i in data]
        print(tweet_list)
        tweets_df = pd.DataFrame(tweet_list, columns = ["Username", "Date", "Time","Tweet ID", "Tweets"])
        tweets_df.to_sql('twitter_data', con = engine, if_exists='replace')
        message = HTML(tweets_df.to_html())
        return render_template("index.html", tables=[tweets_df.to_html()])
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/search', methods = ["GET", "POST"])
def search():
    msg = ''
    conn = sqlite3.connect('twitter.db')
    if request.method == 'POST' and 'keyword' in request.form:
        keyword = request.form['keyword']   
        cur = conn.cursor()
        cur.execute("select * from twitter_data where Tweets like " + "'%" + keyword + "%'")
        rows = cur.fetchall();
        print(rows)
        tweets_df = pd.DataFrame(rows, columns =["Id", "Username", "Date", "Time","Tweet ID", "Tweets"])
        message = HTML(tweets_df.to_html())
        return render_template("index.html", tables=[tweets_df.to_html()])
    elif request.method == 'GET':
        return render_template('search.html')

@app.route('/filters', methods = ["GET", "POST"])
def filters():
    msg = ''
    conn = sqlite3.connect('twitter.db')
    if request.method == 'POST' and 'keyword' in request.form:
        keyword = request.form['keyword'] 
        print(keyword)
        cur = conn.cursor()
        cur.execute("select * from twitter_data where Date = " + "'" + keyword + "'")
        rows = cur.fetchall();
        print(rows)
        tweets_df = pd.DataFrame(rows, columns =["Id", "Username", "Date", "Time","Tweet ID", "Tweets"])
        message = HTML(tweets_df.to_html())
        return render_template("index.html", tables=[tweets_df.to_html()])
    elif request.method == 'GET':
        return render_template('filter.html')
    

# Logout
@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    #db.create_all()
    app.run()