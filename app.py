from flask import Flask, request, render_template, Response, jsonify, redirect, url_for, session
import pickle
import json
import numpy as np
import matplotlib.pyplot as plt
import database as dbase
from  user import User
from prediction import Prediction
from bson.json_util import dumps


db=dbase.dbConnection()

app= Flask(__name__)
app.secret_key = "mysecretkey"

model=pickle.load(open('rf_model.pkl','rb'))

"""@app.route('/prediction',methods=['POST'])
def prediction():
    event = json.loads(request.data)
    values=event['values']
    print(values)
    
    pre=np.array(values)
    res=model.predict(pre)
    print(res)
    return str(res[:3])"""


@app.route('/prediction/<int:npred>',methods=['GET'])
def getnpred(npred):
    return str(npred)

## Prediccion data
@app.route('/data')
def getdata():
    datapred=[]
    predictions=db['prediction']
    for cs in predictions.find({},{'_id':False, 'data_iniSE':False}):
        values=list(cs.values())
        datapred.append(values)
    print(datapred[-6:])
    return jsonify(datapred)


## Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def index():
    predictions=db['prediction']
    casesdata=predictions.find()
    return render_template('index.html', predictions=casesdata)


@app.route('/button', methods=['POST'])
def get_button_status():
    selected_option = request.json['mySelect']
    if selected_option != 'default':
        show_button= True
    else:
        show_button= False
    print(selected_option)
    return jsonify({'show_button': show_button})




## Login View
@app.route('/')
def login():
    return render_template('login.html')

## Register Viz
@app.route('/register')
def register():
    return render_template('register.html')

## Registro Form
@app.route('/registro',methods=['POST'])
def registro():
    users=db['users']
    name=request.form['name']
    email=request.form['email']
    username=request.form['username']
    password=request.form['password']

    if users.find_one({'email': email}):
        error = 'Usuario ya existe.'
    elif name and email and username and password:
        user=User(name, email, password, username)
        users.insert_one(user.toDBCollection())
        response= jsonify({
            'name': name,
            'email': email,
            'password': password,
            'username':username
        })

        return redirect(url_for('login'))

    return render_template('register.html',error=error)

### Login Form
@app.route('/loginin', methods=['GET', 'POST'])
def loginin():
    users=db['users']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})
        if user:
            if (user['password'] == password):
                session['username'] = username
                return redirect(url_for('index'))
        else:
            error = 'Usuario y/o contraseña incorrectos. Intente de nuevo.'
            return render_template('login.html', error=error)    


## Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))





@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ =='__main__':
    app.run(debug=True)

