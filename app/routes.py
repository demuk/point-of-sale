from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.models import userdatastore, security
from app.forms import RegistrationForm
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userdatastore.create_user(username=request.form.get('lastname'),
                                  email=request.form.get('email'), password=request.form.get('password'),
                                  )
        db.session.commit()
        return 'Created account'
    flash('Your account has been created!', 'success')
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')
