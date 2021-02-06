from flask import request, Flask, jsonify, render_template, redirect, json

import utility
from qol_db import db
import clean_data

app = Flask(__name__)
qol = db.Database_QOL()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user = request.form['username']
    password = request.form['password']
    return json.dumps({'status':'OK','user':user,'pass':password})


@app.route('/get_data/crime=<crime>/healthcare=<healthcare>/pollution=<pollution>/restaurant=<restaurant>', methods=['POST'])
def getMapData(crime, healthcare, pollution, restaurant):
    user_in = request.form.get("Crime")
    print('hello')
    print("Crime: " + crime)
    print("Healthcare: " + healthcare)
    print("Pollution: " + pollution)
    print("Restaurant: " + restaurant)
    print('that was it')
    filters = [crime, healthcare, pollution, restaurant]
    data = utility.get_Data(filters)
    return data


@app.route('/life', methods=['GET'])
def get_cities():
    db_json = qol.get_data_test()
    print(db_json)
    return db_json
    

if __name__=="__main__":
    clean_data.request_cost_of_living_rankings()
    qol.database_test()
    app.run(port = 5002)

