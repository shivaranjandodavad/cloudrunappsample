"""
A sample Hello World server.
"""
import os
from flask import Flask,render_template,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn

from flask import Flask, render_template
from sklearn.preprocessing import StandardScaler

model = pickle.load(open('file.pkl','rb'))

# pylint: disable=C0103
app = Flask(__name__)
service = os.environ.get('K_SERVICE', 'Unknown service')
revision = os.environ.get('K_REVISION', 'Unknown revision')

@app.route('/',methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html')
standard_to = StandardScaler()


@app.route('/predict',methods = ['POST'])
def predict():
    Fuel_Type_Diesel =0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 1

        elif(Fuel_Type_Diesel=='Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Year = 2020 - Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual =1
        else:
            Seller_Type_Individual = 0

        Transmission_Manual = request.form['Transmission_Manual']
        if(Transmission_Manual == 'Manual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(prediction[0],2)

        if output<0:
            return render_template('index.html',prediction_text='Sorry! You cannot sell this car')
        else:
            return render_template('index.html', prediction_text='You can sell this car at Rs.{} lakhs'.format(output))

    else:
        return render_template('index.html')



if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
