from app import app, db
from config import *
from app import public_key,private_key
from flask import request,render_template
import requests
import random
from app.models import User,Rollcall
import json
from phe import paillier
from datetime import datetime,date

def random_num_list_generate(n,min_,max_):
    return random.sample(range(min_,max_), n)

@app.route('/api/attendance/<id_>',methods=['GET'])
def get_attendance(id_):
    rollcall = Rollcall.query.filter(Rollcall.id==id_).all()
    print(len(rollcall))
    #print(Rollcall.query.filter(Rollcall.id==id_).count())
    #for x in rollcall:
    #    print (x.id)
    return render_template('attendance_list.html',rollcall=rollcall)

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.get_json();
    if not 'fp' in data or len(data['fp']) != n:
        return({'message':'error'},400)
    fp = data['fp']
    efp_squares=[]
    y_c=[]
    ec=[]

    c_vector=random_num_list_generate(n,1,random_limit)

    for item in fp:
        efp_squares.append(str(public_key.encrypt(item*item).ciphertext()))

    for i in range(0,len(fp)):
        y_c.append(fp[i] - c_vector[i])

    enc_c = [str(public_key.encrypt(x).ciphertext()) for x in c_vector]
    
    #send request to cloud and get back the response

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
        if res==0:
            break

    time_obj = datetime.now()
    time_obj = time_obj.strftime("%H:%M:%S")
    date_obj = date.today()
    date_obj = date_obj.strftime("%d/%m/%y")
    rollcall = Rollcall(id=user.id, date=date_obj, time=time_obj)
    db.session.add(rollcall)
    db.session.commit()

    return({'message':'success'},200)

@app.route('/api/enroll',methods=['POST'])
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
    
    user = User(id=data['id'],b=json.dumps(b_vector))
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
    response = requests.post("http://13.233.17.3:3000/api/enroll", data=data)
    return({'message':'success'},200)
