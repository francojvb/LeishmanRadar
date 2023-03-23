from flask import Flask, request, render_template
import pickle
import json
import numpy as np
import matplotlib.pyplot as plt

app= Flask(__name__)

model=pickle.load(open('rf_model.pkl','rb'))

@app.route('/prediction',methods=['POST'])
def prediction():
    event = json.loads(request.data)
    values=event['values']
    print(values)
    
    pre=np.array(values)
    res=model.predict(pre)
    print(res)
    return str(res[:3])
    
@app.route('/prediction/<int:npred>',methods=['GET'])
def getnpred(npred):
    return str(npred)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

if __name__ =='__main__':
    app.run(debug=True)

