from flask import request, Flask, jsonify, render_template, redirect, json
from qol_db import db
import clean_data

app = Flask(__name__)
qol = db.Database_QOL()

@app.route('/')
def hello():   
    return "Hello World!"

@app.route('/signUp')
def signUp():
    return render_template('index.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username']
    password = request.form['password']
    return json.dumps({'status':'OK','user':user,'pass':password})

@app.route('/life', methods=['GET'])
def get_cities():
    db_json = qol.get_cities_by_user_input(crime_index = 20, health_care_index = 60,pollution_index = 20)
    print(db_json)
    return db_json
    

if __name__=="__main__":
    clean_data.request_cost_of_living_rankings()
    qol.database_test()
    qol.get_cities_by_user_input(20)
    app.run(port = 5002)