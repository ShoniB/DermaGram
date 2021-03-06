from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_wtf import Form
from wtforms import StringField, PasswordField
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)
 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'DontTellAnyone'
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('upload.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

class SignupForm(Form):
    firstname = StringField('firstname')
    lastname = StringField('lastname')
    username = StringField('username')
    address = StringField('address')
    email = StringField('email')
    password = PasswordField('password')
    password2 = PasswordField('password2')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)
   

@app.route("/upload", methods=['GET','POST'])
def upload():
    return render_template('upload.html')

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)