import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SQLALCHEMY_DATABASE_URI =os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'pos.db')
    #SQLALCHEMY_DATABASE_URI = 'postgresql://ndemnvarpwxzda:26e0ee5e0550673ebd6bd039d485de7637b516c82383ac99f755418376ebb757@ec2-3-226-163-72.compute-1.amazonaws.com:5432/d3cvrpfr6tllno'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'kjfdkjfkdjfkdjfkdkdklfjlksjdfkldjfkldf'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
