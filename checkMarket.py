# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 19:33:33 2020

@author: Dylan Pandjaris
"""

import csv
import xlsxwriter
import pyodbc
import datetime
import time
# import pyautogui

import pandas as pd
from selenium import webdriver

# workbook = xlsxwriter.Workbook('Memory.xlsx')

connection = pyodbc.connect('driver={SQL Server};server=DESKTOP-MQ50SL2;database=Stonks')

class Transaction():
    def __init__(self, bought, sold, total, price, portfolioShare, dateTime):
        self.bought = bought
        self.sold = sold
        self.total = total
        self.price = price
        self.portfolioShare = portfolioShare
        self.capital = self.total * self.price
        self.dateTime = dateTime
        
    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.bought, self.sold, self.total, self.price, self.portfolioShare, self.capital, self.dateTime)
        

connectionString = "Server=localhost;Database=master;Trusted_Connection=True;"
server = "DESKTOP-MQ50SL2"
database = "Stonks"

def readData():
    query = 'SELECT * FROM [dbo].[IBD_Trial1]'
    data = pd.read_sql(query, connection)
    for col in data:
        print(col)
    print(data)
        
readData()

def printHead():
    query = 'SELECT * FROM [dbo].[IBD_Trial1]'
    data = pd.read_sql(query, connection)
    print(data.head())

# printHead()

def addTransaction(transaction):
    cursor = connection.cursor()
    cmd = 'INSERT INTO [dbo].[IBD_Trial1] (Bought, Sold, Total, Price, PortfolioShare, Capital) VALUES ({}, {}, {}, {}, {}, {});'
    query = cmd.format(transaction.bought, transaction.sold, transaction.total, transaction.price, transaction.portfolioShare, transaction.capital)
    cursor.execute(query)
    connection.commit()

test = Transaction(5, 0, 5, 20, 100, datetime.datetime.now())
print(test)
# addTransaction(test)

# printHead()

driver = webdriver.Chrome('chromedriver')
driver.get("")
time.sleep(5)
driver.close()









