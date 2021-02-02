from flask import request, Flask, jsonify, render_template, redirect, json
import utility

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


@app.route('/get_data', methods=['POST'])
def getMapData():
    user_in = request.get_json()
    print('hello')
    print(user_in)
    print('that was it')
    filters = [0, 0, 0, 0]
    data = utility.get_Data(filters)
    return data


if __name__=="__main__":
    app.run()