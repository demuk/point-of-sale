from app import app, db,login
from flask import render_template, redirect, url_for, flash, request
# from app.models import userdatastore, security
from app.forms import RegistrationForm
from app.models import User,Product,Shop,Sales
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user,login_required,logout_user
import flask_excel as excel
import string
import secrets
import os



login.login_view='login'

@app.route('/')
@app.route('/index')
@login_required
def index():
    shops=Shop.query.all()
    return render_template('index.html',shops=shops)


@app.route('/home')
def home():
    shops=Shop.query.all()
    products=Product.query.all()
    # for all_prod in products:
    #     pname = all_prod[2]
    #     print(pname)
    qty_prods=Product.query.filter_by(name='Main BOARD').all()
    count = 0
    for prod in qty_prods:
        count+=prod.quantity
    
    return render_template('home.html',products=products,shops=shops)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        alphabet = string.ascii_letters + string.digits
        user_key = ''.join(secrets.choice(alphabet) for i in range(32))
        


        user=User(username=request.form['username'],email=request.form['email'],user_key=user_key, 
            password_hash=generate_password_hash(request.form['password']),location='Nairobi')
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
            return redirect(url_for('index'))
        flash('invalid Username or Password')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/add_product',methods=['GET','POST'])
@login_required
def add_product():
     

    if request.method=='POST':
        # product=Product.query.filter_by(name=request.form['name']).first()
        # if product:
            # if product.status=='not sold'
       
            # prod_to_add = int(request.form['quantity'])
            # product.quantity+=prod_to_add
            # db.session.commit()
            # flash('already exist')
            # return redirect(url_for('home'))


        name=request.form['name']
        alphabet = string.ascii_letters + string.digits
        product_key = ''.join(secrets.choice(alphabet) for i in range(32))
        model = request.form['model']
        buying_price=request.form['buying_price']
        selling_price=0
        quantity=1
        user_id=current_user.id
        shop_id=request.form['shop_id']
        shop= Shop.query.get(shop_id)
        product=Product(name=name,model=model,quantity=quantity,buying_price=buying_price,product_key=product_key,
            selling_price=selling_price,user_id=user_id,shop_id=shop_id)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('view_shop',sk=shop.shop_key))


@app.route('/add_shop',methods=['GET','POST'])
@login_required
def add_shop():
     
        if request.method=='POST':
            alphabet = string.ascii_letters + string.digits
            shop_key = ''.join(secrets.choice(alphabet) for i in range(32))
            name=request.form['shop_name']
            location=request.form['location']
            shop=Shop(name=name,location=location,shop_key=shop_key)
            db.session.add(shop)
            db.session.commit()
            return redirect(url_for('home'))


@app.route('/sell_prod/<pk>', methods=['POST','GET'])
def sell_prod(pk):
    product = Product.query.filter_by(product_key=pk).first()
    if request.method=='POST':
        alphabet = string.ascii_letters + string.digits
        sales_key = ''.join(secrets.choice(alphabet) for i in range(32))
        product.status = 'sold'
        sale=Sales(product_id=product.id,sales_key= sales_key)
        product.selling_price=request.form['selling_price']
        # db.session.add(product)
        db.session.add(sale)
        db.session.commit()
    return redirect(url_for('view_prod',pk=product.product_key))

    
    
@app.route('/inventory')
def inventory():
    products=Product.query.all()
    shops=Shop.query.all()
    return render_template('inventory.html',products=products, shops=shops)

@app.route('/shop_inventory/<sk>')
def shop_inventory(sk):
    # products=Product.query.filter_by(shop_key=sk).first()
    shop=Shop.query.filter_by(shop_key=sk).first()
    # products=Product.query.filter_by(shop_id=shop.id).first()
    return render_template('shop_inventory.html', shop=shop)


    
@app.route('/view_shop/<sk>')
def view_shop(sk):
    shop=Shop.query.filter_by(shop_key=sk).first()
    return render_template('shop.html',shop=shop)


@app.route('/view_prod/<pk>', methods=['POST','GET'])
def view_prod(pk):
    product=Product.query.filter_by(product_key=pk).first()
    return render_template('view_prod1.html',product=product)


@app.route('/delete_prod/<int:id>',methods=['GET','POST'])
def delete_prod(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/edit_product/<int:id>',methods=['GET','POST'])
def edit_product(id):
    product=Product.query.get(id)
    product.name=request.form['name']
    product.model=request.form['model']
    product.buying_price=request.form['buying_price']
    product.selling_price=request.form['selling_price']
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('view_prod',id=id))

@app.route('/sales')
@login_required
def sales():
    sales=Sales.query.all()
    products=Product.query.all()
    return render_template('all_sales.html',sales=sales,products=products)

@app.route('/view_sale/<sk>', methods=['POST','GET'])
def view_sale(sk):
    sale=Sale.query.filter_by(product_key=sk).first()
    return render_template('view_sale.html',sale=sale)


@app.route("/export/<status>", methods=['GET'])
def export(status):
    query_sets= Product.query.filter_by(status=status)
    column_names = ['id', 'name','status','model']
    return excel.make_response_from_query_sets(query_sets, column_names, "xlsx")
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))