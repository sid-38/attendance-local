from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///root:letmein@127.0.0.1:3307/nitc' 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
private_key = None
public_key = None

with open("private_key",'rb') as pvt_file, open("public_key",'rb') as pub_file:
    private_key = pickle.load(pvt_file)
    public_key = pickle.load(pub_file)

from app import routes
from app import models
