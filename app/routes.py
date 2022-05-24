from app import app, db
from flask import render_template, redirect, url_for, flash, request
# from app.models import userdatastore, security
from app.forms import RegistrationForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # userdatastore.create_user(username=request.form['username'],email=request.form['email'],
        #                           password=request.form['password'],location='Nairobi', is_active=True)
        user=User(username=request.form['username'],email=request.form['email'],password_hash=request.form['password'],location='Nairobi')
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    flash('Your account has been created!', 'success')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'])
        if user:
            if check_password_hash(user.password_hash, request.form['password']):
                login_user(user, remember=True)
                return redirect(url_for('home'))
        flash('Confirm Username and Password')
        return redirect(url_for('login'))
    return render_template('login.html')
