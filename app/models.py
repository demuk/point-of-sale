from app import db,app
from flask_security import UserMixin,RoleMixin,SQLAlchemyUserDatastore,Security
from datetime import date

roles_users=db.Table('roles_users',
                     db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                     db.Column('role_id',db.Integer,db.ForeignKey('role.id'))
                     )



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(255))
    is_active=db.Column(db.Boolean)
    created_on=db.Column(db.DateTime,default=date.today())
    roles=db.relationship('Role',secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40))
    description=db.Column(db.String(255))

userdatastore=SQLAlchemyUserDatastore(db,User,Role)
security=Security(app,userdatastore)