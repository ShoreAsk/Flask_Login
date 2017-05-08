# project/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = 'my_precious'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'postgresql://pyflask:pyflask:@localhost:5432/shoretel'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
