from app import app, db
from config import *
from app import public_key,private_key
from flask import request
import random
import json
from app.models import User

def random_num_list_generate(n,min_,max_):
    return random.sample(range(min_,max_), n)

@app.route('/db_test/<id>/<username>')
def db_test(id,username):
    u = User(id=id, username=username)
    db.session.add(u)
    db.session.commit()
    return "Success"

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

@app.route('/enroll',methods=['POST'])
def enroll():
    data = request.get_json()
    print(type(data))
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
    return({'message':'success'},200)
