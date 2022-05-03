from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models import userdatastore, security
from app.forms import RegistrationForm
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
@app.before_first_request
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        userdatastore.create_user(lastname=form.lastname.data, firstname=form.firstname.data, email=form.email.data,
                                  password=form.password.data)
        db.session.add(userdatastore)
        db.session.commit()
        return 'Created account'
    flash('Your account has been created!', 'success')
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')
