from app import app, db
from flask import render_template, redirect, url_for, flash, request
# from app.models import userdatastore, security
from app.forms import RegistrationForm
from app.models import User,Product,Shop,Sales
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user,login_required


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    products=Product.query.all()
    return render_template('home.html',products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':


        user=User(username=request.form['username'],email=request.form['email'],password_hash=generate_password_hash(request.form['password']),location='Nairobi')
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
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if check_password_hash(user.password_hash, request.form['password']):
                login_user(user, remember=True)
            return redirect(url_for('home'))
        flash('invalid Username or Password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/add_product',methods=['GET','POST'])
@login_required
def add_product():

    if request.method=='POST':
        product=Product.query.filter_by(name=request.form['name']).first()
        if product:
            product = Product.quantity
            prod_to_add = request.form['quantity']
            product = prod_to_add + product
            db.session.commit()
            flash('already exist')
            return redirect(url_for('home'))


        name=request.form['name']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']
        quantity=request.form['quantity']
        user_id=current_user.id
        shop_id=1
        product=Product(name=name,quantity=quantity,buying_price=buying_price,selling_price=selling_price,user_id=user_id,shop_id=shop_id)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/add_shop',methods=['GET','POST'])
@login_required
def add_shop():
        if request.method=='POST':
            name=request.form['shop_name']
            location=request.form['location']
            shop=Shop(name=name,location=location)
            db.session.add(shop)
            db.session.commit()
            return redirect(url_for('home'))


@app.route('/sell_prod/<int:id>', methods=['POST','GET'])
def sell_prod(id):
    product = Product.query.get(id)
    product.status = 'sold'
    sale=Sales(product_id=id)
    db.session.add(sale)
    db.session.commit()
    return redirect(url_for('view_prod',id=id))



@app.route('/view_prod/<int:id>', methods=['POST','GET'])
def view_prod(id):
    product=Product.query.get(id)
    return render_template('view_prod.html',product=product)


@app.route('/delete_prod/<int:id>',methods=['GET','POST'])
def delete_prod(id):
    product=Product.query.get(id)
    product.quantity -=1
    db.session.commit()
    return redirect(url_for('home'))
