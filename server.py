from flask import request, Flask, jsonify, render_template, redirect, json

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/signUp')
def signUp():
    return render_template('index.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

if __name__=="__main__":
    app.run()