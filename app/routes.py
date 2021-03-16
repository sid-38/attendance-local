from app import app, db
from config import *
from app import public_key,private_key
from flask import request
import requests
import random
from app.models import User
import json
from phe import paillier


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
    # efp = []
    # for item in fp:
    #     efp.append(public_key.encrypt(item))
    efp_squares=[]
    y_c=[]
    c_list=[]
    ec=[]
    for item in fp:
        efp_squares.append(str(public_key.encrypt(item*item).ciphertext()))
    c_vector=random_num_list_generate(n,1,random_limit)
    for i in range(0,len(fp)):
        y_c.append(fp[i] - c_vector[i])
    enc_c = [str(public_key.encrypt(x).ciphertext()) for x in c_vector]
    # y_c.append(item-c)
    # ec.append(public_key.encrypt(c))
        #send request to cloud
        #get back the response
    data = {"enc_y2":efp_squares, "y_c":y_c, "enc_c":enc_c}
    enc = json.JSONEncoder()
    data = enc.encode(data)
    response = requests.post("http://13.233.17.3:3000/api/verify", data)
    response_json = response.json()
    for k in response_json:
        tid = paillier.EncryptedNumber(public_key, int(k))
        res = paillier.EncryptedNumber(public_key, int(response_json[k]))
        tid_d= private_key.decrypt(tid)
        user = User.query.filter_by(tid=tid_d).first()
        b_vector = json.loads(user.b)
        extra = 0
        for i in range(0,len(b_vector)):
            extra += 2*b_vector[i]*c_vector[i]

        res = private_key.decrypt(res) - extra
        print(res)
        print(user.id, user.b)

    return({'message':'success'},200)

@app.route('/enroll',methods=['POST'])
def enroll():
    data = request.get_json();
    if not 'id' in data or not 'fp' in data or len(data['fp']) != n:
        return({'message':'error'},400)
    fp = data['fp']
    esfp = []
    b_vector = []
    diff_array = []
    
    #Generate ids and store it in database
    b_vector=random_num_list_generate(n,1,random_limit)
    print(b_vector)
    user = User(id=data['id'], b=json.dumps(b_vector))
    db.session.add(user)
    db.session.commit()

    #Prepare data to be sent to cloud
    for item in fp:
        item_s=item*item
        esfp.append(str(public_key.encrypt(item_s).ciphertext()))

    for i in range(0,len(fp)):
        diff_array.append(fp[i]-b_vector[i])
    
    b_enc = [str(public_key.encrypt(x).ciphertext()) for x in b_vector]
    tid_enc = str(public_key.encrypt(int(user.tid)).ciphertext())
    data = {'enc_x2':esfp, 'x_b':diff_array, 'enc_b':b_enc, 'enc_tid':tid_enc}
    enc = json.JSONEncoder()
    data = enc.encode(data)
    # print(data)
    response = requests.post("http://13.233.17.3:3000/api/enroll", data=data)

    # requests.post('http://13.233.17.3:3000/api/enroll', json={})

    return({'message':'success'},200)