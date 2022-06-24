import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    	'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'pos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'kjfdkjfkdjfkdjfkdkdklfjlksjdfkldjfkldf'

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
