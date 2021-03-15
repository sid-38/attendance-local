from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from phe import paillier
import pickle
import json
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///root:letmein@127.0.0.1:3307/nitc'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
private_key = None
public_key = None
n = 3;
random_limit = 10

with open("private_key",'rb') as pvt_file, open("public_key",'rb') as pub_file:
    private_key = pickle.load(pvt_file)
    public_key = pickle.load(pub_file)

def random_num_list_generate(n,min_,max_):
    return random.sample(range(min_,max_), n)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json();
    if not 'fp' in data or len(data['fp']) != n:
        return({'message':'error'},400)
    fp = data['fp']
    efp = []
    for item in fp:
        efp.append(public_key.encrypt(item))

    return({'message':'success'},200)

<<<<<<< HEAD
from app import models
=======
@app.route('/enroll',methods=['POST'])
def enroll():
    data = request.get_json();
    if not 'id' in data or not 'fp' in data or len(data['fp']) != n:
        return({'message':'error'},400)
    fp = data['fp']
    esfp = []
    b_vector = []
    diff_array = []
    for item in fp:
        item_s=item*item
        esfp.append(public_key.encrypt(item_s))
    print(esfp)
    b_vector=random_num_list_generate(n,1,random_limit)
    print(b_vector)
        # diff_array.append(item-ran)
    # while(1):
    #     tid=random.randint(100,300)
    #     public_key.encrypt(tid)

    return({'message':'success'},200)


>>>>>>> kavya
