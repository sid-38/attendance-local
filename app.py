from flask import Flask, request;
app = Flask(__name__)

@app.route('/verify', methods=['POST'])
def verify():
    name = request.get_json();
    print(name);
    return({'message':'success'},200);
