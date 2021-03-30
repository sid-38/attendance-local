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
from multiprocessing import Manager,Process,Queue
import time

def random_num_list_generate(n,min_,max_):
    return random.sample(range(min_,max_), n)
    
def worker(enc_tid,enc_res,pub_key,pvt_key,return_dict):
    tid = paillier.EncryptedNumber(pub_key, int(enc_tid))
    res = paillier.EncryptedNumber(pub_key, int(enc_res))
    return_dict[pvt_key.decrypt(tid)]=pvt_key.decrypt(res)
        
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
    t0=time.time()
    data = request.get_json();
    if not 'fp' in data or len(data['fp']) != n:
        return({'message':'error'},400)
    fp = data['fp']
    efp_squares=[]
    y_c=[]
    ec=[]

    c_vector=random_num_list_generate(n,1,random_limit)
    e_0 = public_key.encrypt(0)

    for item in fp:
        efp_squares.append(str((e_0 + item*item).ciphertext(False)))
        # efp_squares.append(str(public_key.encrypt(item*item).ciphertext()))

    for i in range(0,len(fp)):
        y_c.append(fp[i] - c_vector[i])

    # enc_c = [str(public_key.encrypt(x).ciphertext()) for x in c_vector]
    enc_c = [str((e_0 + x).ciphertext(False)) for x in c_vector]
    
    t1=time.time()
    #send request to cloud and get back the response

    data = {"enc_y2":efp_squares, "y_c":y_c, "enc_c":enc_c}
    enc = json.JSONEncoder()
    data = enc.encode(data)
    response = requests.post("http://13.233.17.3:3000/api/verify", data)
    response_json = response.json()
    t2=time.time()
    
    res_dict={}
    jobs=[]
    manager=Manager()
    return_dict=manager.dict()
    for k in response_json:
        res_dict[k]=response_json[k]
        p=Process(target=worker,args=(k,response_json[k],public_key,private_key,return_dict))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()
        
    t3=time.time()
    
    users = User.query.all()
    user_b = {user.tid: (user.b,user.id) for user in users}
    print(user_b)
    for tid in return_dict:
        # user=User.query.filter_by(tid=tid).first()
        print(tid,type(tid))
        b_vector = json.loads(user_b[str(tid)][0])
        uid = user_b[str(tid)][1]
        extra = 0
        found = False
        for i in range(0,len(b_vector)):
            extra += 2*b_vector[i]*c_vector[i]
        res =return_dict[tid]- extra
        if res<threshold:
            found=True
            break
    
    '''for k in response_json:
        tid = paillier.EncryptedNumber(public_key, int(k))
        res = paillier.EncryptedNumber(public_key, int(response_json[k]))
        tid_d= private_key.decrypt(tid)
        user = User.query.filter_by(tid=tid_d).first()
        b_vector = json.loads(user.b)
        extra = 0
        found = False
        for i in range(0,len(b_vector)):
            extra += 2*b_vector[i]*c_vector[i]
        res = private_key.decrypt(res) - extra
        if res<threshold:
            found = True
            break'''
    t4=time.time()
    if found:
        time_obj = datetime.now()
        time_obj = time_obj.strftime("%H:%M:%S")
        date_obj = date.today()
        date_obj = date_obj.strftime("%d/%m/%y")
        rollcall = Rollcall(id=uid, date=date_obj, time=time_obj)
        db.session.add(rollcall)
        db.session.commit()
        t5=time.time()
        print("Total:",t5-t0)
        print("Encryption:",t1-t0)
        print("Cloud RTT:",t2-t1)
        print("Decryption(M):",t3-t2)
        print("Decryption:",t4-t3)
        print("Cryptdb:",t5-t4)
        return({'message':'success'},200)
    
    return({'message':'failed'}, 403)

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

    e_0 = public_key.encrypt(0)
   
    #Prepare data to be sent to cloud
    for item in fp:
        item_s=item*item
        # esfp.append(str(public_key.encrypt(item_s).ciphertext()))
        esfp.append(str((e_0 + item_s).ciphertext(False)))

    for i in range(0,len(fp)):
        diff_array.append(fp[i]-b_vector[i])

    # b_enc = [str(public_key.encrypt(x).ciphertext()) for x in b_vector]
    b_enc = [str((e_0+x).ciphertext(False)) for x in b_vector]
    tid_enc = str(public_key.encrypt(int(user.tid)).ciphertext())
    data = {'enc_x2':esfp, 'x_b':diff_array, 'enc_b':b_enc, 'enc_tid':tid_enc}

    enc = json.JSONEncoder()
    data = enc.encode(data)
    response = requests.post("http://13.233.17.3:3000/api/enroll", data=data)
    
    return({'message':'success'},200)