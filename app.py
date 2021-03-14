from flask import Flask, request
from phe import paillier
import pickle
import json
import random

app = Flask(__name__)
private_key = None
public_key = None
n = 3;
random_limit = 10

with open("private_key",'rb') as pvt_file, open("public_key",'rb') as pub_file:
    private_key = pickle.load(pvt_file)
    public_key = pickle.load(pub_file)

def random_num_generate(n):
    return random.sample(range(1,random_limit), n)

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
        while(1):
            ran=random.randint(0,25)
            if (item-ran) > 0:
                break
        diff_array.append(item-ran)
        b_vector.append(ran)
    #template id should be generated... which is unique to each user
    while(1):
        tid=random.randint(100,300)
        #check if this already exists by going through all mysql entries
        #if not continue
        public_key.encrypt(tid)

    return({'message':'success'},200)


