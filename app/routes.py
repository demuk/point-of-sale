from app import app, db
from flask import render_template, redirect, url_for, flash, request
# from app.models import userdatastore, security
from app.forms import RegistrationForm
from app.models import User,Product,Shop,Sales
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user,login_required,logout_user
import flask_excel as excel


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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
        # product=Product.query.filter_by(name=request.form['name']).first()
        # if product:
            # if product.status=='not sold'
       
            # prod_to_add = int(request.form['quantity'])
            # product.quantity+=prod_to_add
            # db.session.commit()
            # flash('already exist')
            # return redirect(url_for('home'))


        name=request.form['name']
        model = request.form['model']
        buying_price=request.form['buying_price']
        selling_price=0
        quantity=1
        user_id=current_user.id
        shop_id=request.form['shop_id']
        product=Product(name=name,model=model,quantity=quantity,buying_price=buying_price,selling_price=selling_price,user_id=user_id,shop_id=shop_id)
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
    if request.method=='POST':
        product.status = 'sold'
        sale=Sales(product_id=id)
        product.selling_price=request.form['selling_price']
        # db.session.add(product)
        db.session.add(sale)
        db.session.commit()
    return redirect(url_for('view_prod',id=id))

    
    
    
    
    



@app.route('/view_prod/<int:id>', methods=['POST','GET'])
def view_prod(id):
    product=Product.query.get(id)
    profit=product.selling_price-product.buying_price
    return render_template('view_prod.html',product=product,profit=profit)


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
    return render_template('sales.html',sales=sales,products=products)


@app.route("/export", methods=['GET'])
def export():
    query_sets= Product.query.all()
    column_names = ['id', 'name','status','model']
    return excel.make_response_from_query_sets(query_sets, column_names, "xlsx")
    return redirect(url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))