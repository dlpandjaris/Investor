# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 00:50:02 2020

@author: Dylan Pandjaris
"""

# import pyodbc
import time
import datetime
import xlsxwriter
from openpyxl import load_workbook
from selenium import webdriver

import pandas as pd
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

from sklearn.svm import SVC
from sklearn import metrics
import matplotlib.pyplot as plt
from addAMD import Daily_data

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers

# connection = pyodbc.connect('driver={SQL Server};server=DESKTOP-MQ50SL2;database=Stonks')

def process_range(delta):
    low = ""
    high = ""
    spaces = 0
    for char in delta:
        if spaces == 0:
            low += char
        if spaces == 2:
            high += char
        if char == " ":
            spaces += 1
    low = float(low[:-1])
    high = float(high)
    return([low, high])
            
def process_percent(delta):
    percent = ''
    go = False
    for char in delta:
        if go:
            if char != "%":
                percent += char
        if char == "(":
            go = True
    print("Percent:", percent)
    
def process_volume(string):
    vol = ""
    for char in string:
        if char != ",":
            vol += char
    return(int(vol))

def get_day():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://finance.yahoo.com/quote/AMD?p=AMD")
    driver.maximize_window()
    
    date = datetime.datetime.now().date()
    _open = driver.find_element_by_xpath(r'//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span')
    _open = float(_open.text)
    delta = driver.find_element_by_xpath(r'//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]')
    delta = delta.text
    low = process_range(delta)[0]
    high = process_range(delta)[1]
    close = driver.find_element_by_xpath(r'//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')
    close = float(close.text)
    volume = driver.find_element_by_xpath(r'//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span')
    volume = process_volume(volume.text)
    
    day = Daily_data(date, _open, high, low, close, volume)
    driver.close()
    
    return(day)
    
# day = get_day()
# print(day)

def get_data():
    query = 'SELECT * FROM [dbo].[AMD]'
    data = pd.read_sql(query, connection)
    # print(data.head())
    
    return(data)
    
def evaluate_stock():
    data = pd.read_csv("AMD_Processed.csv", delimiter=",")
    keys = []
    values = []
    toms_predictors = []
    for i in range(len(data)):
        values.append([])
    
    days = 5
    for index, row in data.iterrows():
        if index >= days:
            keys.append(row["Delta"])
            for i in range(days):
                values[index-i].append(row["Open"])
                values[index-i].append(row["High"])
                values[index-i].append(row["Low"])
                values[index-i].append(row["Close"])
                values[index-i].append(row["Volume"])
                values[index-i].append(row["Delta"])
        if index < -days:
            print(index)
    
    
            
    values = values[days:len(data)-days]
    keys = keys[days:]
    
    col_names = []
    for i in range(len(values[0])):
        col_names.append("x" + str(i))
    col_names.append("Y")
    
    col_data = []
    for i in range(len(col_names)):
        col_data.append([])
    
    for i in range(len(values)):
        for j in range(len(values[i])):
            col_data[j].append(values[i][j])
        col_data[-1].append(keys[i])    
        
        # if keys[i] > 0:
        #     col_data[-1].append(1)
        # else:
        #     col_data[-1].append(0)
    
    df = {}
    for i in range(len(col_names)):
        df[col_names[i]] = col_data[i]
    
    
    
    
    data_frame = pd.DataFrame(df, columns = col_names)
    
    X = data_frame[col_names[:-1]]
    Y = data_frame['Y']
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    
    model = LinearRegression(fit_intercept = True, normalize = True, copy_X = True)
    model = model.fit(X_train, Y_train)

    coefs = model.coef_
    # print(X_train)
    
    def predict_Y(index):
        sumi = 0
        for i in range(len(coefs)):
            coef = "x" + str(i)
            # print(X_test[coef][index])
            sumi += coefs[i] * X_test[coef][index]
        # sumi /= len(coefs)
        return(sumi)
    
    # print(abs(predict_Y(109) - Y_test[109]))
    def get_accuracy_array():
        all_acc = []
        for i in range(len(data)):
            try:
                trial_diff = abs(predict_Y(i) - Y_test[i])
                all_acc.append(trial_diff)
            except KeyError:
                pass
        acc = []
        for accuracy in all_acc:
            if accuracy != -100:
                acc.append(accuracy)
        return(acc)
    
    # print(get_accuracy_array())
    
    def mean_squared_error():
        error = get_accuracy_array()
        sumi = []
        for num in error:
            sumi.append(num ** 2)
        return(sum(sumi) / len(error))
    
    print(mean_squared_error())
            
    # expected = model.predict(X_test)
    # print(expected)
    # print(model.score(X_test, Y_test))
    # print(Y_test)
    
    # for i in range(len(values)):
        
    
    # for i in range(len(expected)):
    #     print(i, Y_test[i])
        #print("Expected:", expected[i], "   Actual:", Y_test[i])
    
    # svc = SVC.fit(X_train,y_train)
    
    # logistic_regression = LogisticRegression().fit(X_train,y_train)
    # y_pred = logistic_regression.predict(X_test)    
    
    # confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
    # sn.heatmap(confusion_matrix, annot=True)
    
    # accuracy = metrics.accuracy_score(y_test, y_pred)
    # print('Accuracy: ', accuracy)
    # plt.show()

evaluate_stock()



# train_df = data_frame.sample(frac = 0.8, random_state=0)
# test_df = data_frame.drop(train_df.index)

# # sns.pairplot(train_df[col_names], diag_kind="kde")

# train_stats = train_df.describe()
# train_stats = train_stats.transpose()

# # print(train_stats)

# def norm(x):
#     return((x - train_stats['mean']) / train_stats['std'])

# norm_train_df = norm(train_df)
# norm_test_df = norm(test_df)

# def build_model():
#     model = keras.Sequential([
#         layers.Dense(64, activation=keras.activations.relu, input_shape=[len(train_df.keys())]),
#         layers.Dense(64, activation=keras.activations.relu),
#         layers.Dense(1)
#         ])
    
#     optimizer = keras.optimizers.RMSprop(0.001)
#     model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
    
#     return(model)

# model = build_model()
# # model.summary()

# class PrintDot(keras.callbacks.Callback):
#     def on_epoch_end(self, epoch, logs):
#         if epoch % 100 == 0:
#             print('')
#             print('.', end='')
            
# EPOCHS = 1000

# print(norm_train_df)
# history = model.fit(
#     norm_train_df, train_df.keys(),
#     epochs=EPOCHS, validation_split=0.2, verbose=0)

# connection.close()

def add_to_data_table(day):
    new_row = [day.date, day.open, day.high, day.low, day.close, day.volume, day.pps, day.delta]
    workbook = load_workbook("AMD_Processed.xlsx")
    worksheet = workbook.worksheets[0]
    worksheet.append(new_row)
    workbook.save("AMD_Processed.xlsx")

# add_to_data_table(day)

