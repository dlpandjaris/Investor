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

connection = pyodbc.connect('driver={SQL Server};server=#######-#######;database=######')

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
        

connectionString = "Server=localhost;Database=######;Trusted_Connection=True;"
server = "######-######"
database = "######"

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

def robinhoodLogin():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://robinhood.com/us/en/")
    driver.maximize_window()
    
    login = driver.find_element_by_xpath(r'//*[@id="root"]/div[2]/nav/div/div[4]/a[1]/span/span')
    login.click()
    
    username = driver.find_element_by_xpath(r'//*[@id="react_root"]/div[1]/div[2]/div/div[2]/div/div/form/div/div[1]/div[1]/label/div[2]/input')
    username.send_keys("########@email.com")
    
    password = driver.find_element_by_xpath(r'//*[@id="react_root"]/div[1]/div[2]/div/div[2]/div/div/form/div/div[1]/div[2]/label/div[2]/input')
    password.send_keys("#########")
    
    sign_in = driver.find_element_by_xpath(r'//*[@id="react_root"]/div[1]/div[2]/div/div[2]/div/div/form/footer/div/button')
    sign_in.click()
    
    time.sleep(2)
    email_me = driver.find_element_by_xpath(r'//*[@id="react_root"]/div[1]/div[2]/div/div[2]/div/div/div/footer/div[2]/button/span')
    email_me.click()
    
    time.sleep(20)
    code = checkEmail.getCode()
    print(code)
    
    codeInput = driver.find_element_by_xpath(r'//*[@id="react_root"]/div[1]/div[2]/div/div[2]/div/div/div/form/input')
    codeInput.send_keys(code)
    
    confirm = driver.find_element_by_xpath(r'//*[@id="react_root"]/div[1]/div[2]/div/div[2]/div/div/div/form/footer/div[2]/button')
    # confirm.click(
    
    # time.sleep(5)
    # driver.close()

robinhoodLogin()


