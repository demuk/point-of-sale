# from sqlalchemy import ForeignKey

from app import db
from app import login
from flask_login import  UserMixin
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    location = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    created_on = db.Column(db.DateTime, default=date.today())
    # roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    status=db.Column(db.String(55),default='normal')
    products=db.relationship('Product',backref='dealer',lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    products = db.relationship('Product', backref='shop', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    model = db.Column(db.String(255))
    quantity = db.Column(db.Integer())
    buying_price = db.Column(db.Integer())
    selling_price = db.Column(db.Integer())
    status=db.Column(db.String(55),default='not sold')
    user_id= db.Column(db.Integer,db.ForeignKey('user.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    sales = db. relationship('Sales', backref='product', lazy=True)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    receipt = db.relationship('Receipt', backref='receipt', lazy=True)


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    sale_id=db.Column(db.Integer,db.ForeignKey('sales.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# userdatastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, userdatastore)
