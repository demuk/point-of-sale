import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SQLALCHEMY_DATABASE_URI = 'postgres://bnhxyunkwohjxf:edfa41baf5f188be4ca7ef8e78f2fd2d3a53003590a1e5bb92a31e688f1c1165@ec2-23-23-182-238.compute-1.amazonaws.com:5432/d5jlnsibam9772' \
        'sqlite:///' + os.path.join(basedir, 'pos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'kjfdkjfkdjfkdjfkdkdklfjlksjdfkldjfkldf'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
