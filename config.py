import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SQLALCHEMY_DATABASE_URI ='postgres://crctunmilxytsj:fa0d794ddd4958c25aa886e4a0ab94c0f124110fae22339384801c9f79586a2e@ec2-3-219-229-143.compute-1.amazonaws.com:5432/d5gb8kbn46q6du'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://ndemnvarpwxzda:26e0ee5e0550673ebd6bd039d485de7637b516c82383ac99f755418376ebb757@ec2-3-226-163-72.compute-1.amazonaws.com:5432/d3cvrpfr6tllno'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'kjfdkjfkdjfkdjfkdkdklfjlksjdfkldjfkldf'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
