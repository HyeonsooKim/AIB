import pandas as pd
import numpy as np
import os
# import FinanceDataReader as fdr
import sqlite3
from bs4 import BeautifulSoup
import urllib.request as req
import joblib

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
#평가지표
from sklearn.metrics import accuracy_score, plot_confusion_matrix, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.metrics import roc_curve, classification_report, roc_auc_score, r2_score, mean_absolute_error

from samsung_stock_db import sample

conn = sqlite3.connect('project3.sqlite3')
cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS Prediction""")
cur.execute("""CREATE TABLE Prediction (
               'Date' DATE,
               origin INTEGER,
               predict INTEGER);
    """)

model = LinearRegression()
# model = Ridge(alpha=1, solver='cholesky')
# model = Lasso(alpha=0.1)

data = sample

x = data.iloc[0:-2].to_numpy() # 2주 전까지의 데이터로
y = data.iloc[1:-1].to_numpy() # 각 주의 다음 주의 데이터를 예측한다
y_0 = y[:,0]
y_1 = y[:,1]
y_2 = y[:,2]
y_3 = y[:,3]
y_4 = y[:,4]

y_values = [y_0, y_1, y_2, y_3, y_4]
x_public = data.iloc[-5].to_numpy() # 3주전 데이터를 예측할 것이다

predictions = []
for y_value in y_values :
    model.fit(x,y_value)
    prediction = model.predict(np.expand_dims(x_public,0))
    predictions.append(round(prediction[0]))

origin = []
for i in data.iloc[-4]:
    origin.append(i)

print("Data for 20 September to 25 September")
print("Original Data: ", origin)
print("Predict  Data: ", round(predictions))

joblib.dump(model, 'model_211012.pkl')


