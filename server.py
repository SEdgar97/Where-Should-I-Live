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


@app.route('/get_data/crime=<crime>/healthcare=<healthcare>/pollution=<pollution>/restaurant=<restaurant>', methods=['POST'])
def getMapData(crime, healthcare, pollution, restaurant):
    user_in = request.form.get("Crime")
    print('hello')
    print("Crime: " + crime)
    print("Healthcare: " + healthcare)
    print("Pollution: " + pollution)
    print("Restaurant: " + restaurant)
    print('that was it')
    filters = [0, 0, 0, 0]
    data = utility.get_Data(filters)
    return data


if __name__=="__main__":
    app.run()