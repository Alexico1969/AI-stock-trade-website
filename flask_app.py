
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
import locale
import sqlite3

app=Flask(__name__, static_url_path='/static')

app.secret_key = 'Bruce Wayne is Batman'

locale.setlocale( locale.LC_ALL, '' )

# Database connection
DATABASE = 'flask_app.db'
conn = sqlite3.connect(DATABASE, check_same_thread=False)
c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS vals (id INTEGER PRIMARY KEY, money INTEGER, stock INTEGER, course INTEGER) ''')
c.execute(''' SELECT * FROM vals ''')
data = c.fetchall()

if len(data) == 0:
    c.execute(''' INSERT INTO vals (money, stock, course) VALUES (100000, 0, 115.90) ''')
    conn.commit()
    c.execute(''' SELECT * FROM vals ''')
    data = c.fetchall()


money = data[0][1]
stock = data[0][2]
course = data[0][3]

c.execute(''' CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, log TEXT) ''')

conn.commit()

@app.route('/', methods=['GET', 'POST'])
def home_page():
    global money, stock, course, c
    log_text = ""
    
    if request.method == 'POST':
        log_text = ""
        action = request.form['action']
        value = request.form['value']
        if action == 'buy':
            stock = int(money / course)
            money = money % course
            log_text = "Bought " + str(stock) + " shares at " + str(course)
        elif action == 'sell':
            money = round(money + stock * course,2)
            stock = 0
            log_text = "Sold " + str(stock) + " shares at " + str(course)
        elif action == 'update':
            course = float(value)
            log_text = "Updated course to " + str(course)
        elif action == 'a-money':
            money = float(value)
            log_text ="Adjusted money value to:",money
        elif action == 'a-stock':
            stock = int(value)
            log_text = "Adjusted stock value to:",stock
        elif action == 'comment':
            log_text = "Comment: " + value
        
    money_f = locale.currency(money, grouping=True)
    value_f = locale.currency(stock*course, grouping=True)
    total_f = locale.currency(money + stock*course, grouping=True)

    c.execute(''' UPDATE vals SET money = ?, stock = ?, course = ? ''', (money, stock, course))
    conn.commit()

    if log_text != "":
        c.execute(''' INSERT INTO log (log) VALUES (?) ''', (str(log_text),))
        log_text = ">> CURRENT VALUES: money: " + str(money_f) + " - stock: " + str(stock) + " - course: " + str(course) + " - stock value: " + str(value_f) + " - total value: " + str(total_f)
        c.execute(''' INSERT INTO log (log) VALUES (?) ''', (log_text,))
        conn.commit()

    c.execute(''' SELECT * FROM log ''')
    log = c.fetchall()
    log.reverse()

    
    return render_template('home.html', money=money_f, stock=stock, course=course, value=value_f, total=total_f, log=log)

@app.route('/login', methods=['GET', 'POST'])
def login():
   return "login"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return "signup"

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))

# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    if flask_env != 'production':
        environ['FLASK_ENV'] = 'development'
        app.debug = True
        app.asset_debug = True
        server = Server(app.wsgi_app)
        server.serve()
    app.run()

