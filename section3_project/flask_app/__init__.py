from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse
from urllib import request, parse

import webbrowser
import joblib
import requests
import json

from predict_model import predictions, data

def start_app(self):

    app = Flask(__name__)
    model = joblib.load('model_211012.pkl')
    @app.route('/')
    def index():
        return "Hello", 200

    #예측 결과
    @app.route('/predicts')
    def results():
        return predictions, 200
    
    #원래 값
    @app.route('/data')
    def disp():
        return data.iloc[-1], 200
    
    #그래프?
    @app.route('/dashboard')
    def disp_dash():
        url = "http://localhost:3000/dashboard/2-samsung-stock-price-trend"
        return requests.get(url), 200
    #메트릭들 MAE나 R-squared

    return app


# def create_app(self):

#     app = Flask(__name__)
    
#     service_key = "nVbikKzKoaDk%2Fs7WHF%2FI6%2FdAQqi03h%2FKKhHtBkVmlt%2FXdG4KnqCR0VcX90iwjRvO6KadGUmAkl9JaDSnLHd%2Bjg%3D%3D"
#     ldcode = "1168010100"
#     year = "2019"
#     url = "http://apis.data.go.kr/1611000/nsdi/ReferLandPriceService/attr/getReferLandPriceAttr?ServiceKey={service_key}&ldCode={ldcode}&stdrYear={year}&format=xml&numOfRows=10&pageNo=1"

#     @app.route('/')
#     def index():
#         return requests.get(url).text, 200
    
#     return app

# service_key = "nVbikKzKoaDk%2Fs7WHF%2FI6%2FdAQqi03h%2FKKhHtBkVmlt%2FXdG4KnqCR0VcX90iwjRvO6KadGUmAkl9JaDSnLHd%2Bjg%3D%3D"
# ldcode = "1168010100"
# year = "2019"
# url = "http://apis.data.go.kr/1611000/nsdi/ReferLandPriceService/attr/getReferLandPriceAttr?ServiceKey={service_key}&ldCode={ldcode}&stdrYear={year}&format=xml&numOfRows=10&pageNo=1"

# dd = requests.get(url)
# print(dd.status_code)