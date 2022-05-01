from app import app
from flask import render_template, redirect


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
