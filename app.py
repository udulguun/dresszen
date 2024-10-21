# import os
# import sys
# sys.path.insert(0, '/home/udulguun/public_html/dresszen/env/lib/python3.12/site-packages')

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt

import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "new_password"
app.config['MYSQL_DB'] = "udulguun_db"

import mysql.connector

mysql_client = mysql.connector.connect(
    host="localhost",
    user="root",
    password="new_password",
    database="dresszenfinder5"
)

@app.route('/', methods=['GET', 'POST'])
def register():  # Changed function name from `index` to `register`
    if request.method == 'POST':
        username = request.form['username']
        size = request.form['size']
        age = request.form['age']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']

        cur = mysql_client.cursor()
        cur.execute("INSERT INTO users(username, size, age, email, gender, password) VALUES(%s, %s, %s, %s, %s, %s)", 
                    (username, size, age, email, gender, password))
        mysql_client.commit()
        cur.close()

        flash("User added successfully!", "success")  # Flash a success message
        return redirect(url_for('register'))  # Changed redirection to `register`

    return render_template('register.html')


@app.route('/tops')
def tops():
    return render_template('tops.html')

@app.route('/bottoms')
def bottoms():
    return render_template('bottoms.html')

@app.route('/shoes')
def shoes():
    return render_template('shoes.html')

@app.route('/acc')
def acc():
    return render_template('acc.html')

@app.route('/brands')
def brands():
    return render_template('brands.html')

@app.route('/saved')
def saved():
    return render_template('saved.html')

@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')


@app.route('/index')  # The second `index` function is kept here
def index():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('signin'))  # Redirect to sign-in if not logged in

@app.route('/signout')
def signout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql_client.cursor()
        cur.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        record = cur.fetchone()

        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('index'))  # Redirect to the main index page
        else:
            msg = 'Incorrect username or password'

    return render_template('signin.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
