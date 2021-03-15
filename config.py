import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql:///root:letmein@127.0.0.1:3307/nitc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

n = 3;
random_limit = 10
