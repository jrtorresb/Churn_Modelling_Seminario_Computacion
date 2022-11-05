#importing libraries
import os
import numpy as np
import pandas as pd
import flask
import pickle
from flask import Flask, render_template, request, jsonify

#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"STATUS": "UP"})


def ValuePredictor(to_predict_list):
    #to_predict = np.array(to_predict_list).reshape(1, 4)
    loaded_model = pickle.load(open("api/model.pkl", "rb"))
    result = loaded_model.predict(to_predict_list)
    return result[0]


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        print(request.form.to_dict())
        to_predict_list = pd.DataFrame(to_predict_list, index=[0])
        #to_predict_list = list(to_predict_list.values())

        try:
            #to_predict_list = list(map(float, to_predict_list))
            result = ValuePredictor(to_predict_list)
            if int(result) == 0:
                prediction = 'Es probable que el cliente no abandone la institución'
            elif int(result) == 1:
                prediction = '¡URGENTE!  Es probable que el cliente abandone la institución'
            else:
                prediction=f'{int(result)} No-definida'
        except ValueError:
            prediction = 'Error en el formato de los datos'

        return render_template("result.html", prediction=prediction)


if __name__=="__main__":
    app.run(debug=True, host='127.0.0.1', port=5002)