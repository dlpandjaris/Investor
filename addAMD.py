# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 22:44:21 2020

@author: Dylan Pandjaris
"""

import csv
import pyodbc
import datetime

import pandas as pd

class Daily_data():
    def __init__(self, date, _open, high, low, close, volume):
        self.date = date
        self.open = _open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.pps = self.profit_per_share()
        self.delta = self.delta()

    def profit_per_share(self):
        return(self.close - self.open)
        
    def delta(self):
        return((self.profit_per_share()/self.open))
    
    def __str__(self):
        return("{} {} {} {} {} {} {} {}".format(self.date, self.open, self.high, self.low, self.close, self.volume, self.pps, self.delta))


# print(datetime.datetime.now().date())


data = []
with open("AMD.csv") as csvfile:
    readcsv = csv.reader(csvfile, delimiter = ",")
    cnt = 1
    for row in readcsv:
        cnt += 1
        if cnt > 2:
            date = row[0]
            _open = float(row[1])
            high = float(row[2])
            low = float(row[3])
            close = float(row[4])
            volume = int(row[6])
            data.append(Daily_data(date, _open, high, low, close, volume))
            
# print(data[0].date)
# print(data[1].date)

# connection = pyodbc.connect('driver={SQL Server};server=DESKTOP-MQ50SL2;database=Stonks')

def add_day(row):
    this = data[row]
    cursor = connection.cursor()
    cmd = 'INSERT INTO [dbo].[AMD] (Date, [Open], High, Low, [Close], Volume, PPS, Delta) VALUES ({}, {}, {}, {}, {}, {}, {}, {});'
    query = cmd.format(this.date, this.open, this.high, this.low, this.close, this.volume, this.pps, this.delta)
    cursor.execute(query)
    connection.commit()
    
def printHead():
    query = 'SELECT * FROM [dbo].[AMD]'
    data = pd.read_sql(query, connection)
    print(data.head())
    
def delete_all():
    cursor = connection.cursor()
    cmd = 'DELETE FROM [dbo].[AMD] WHERE Date != 2030-00-00'
    cursor.execute(cmd)
    connection.commit()

def export_csv():
    col_names = ["Date", "Open", "High", "Low", "Close", "Volume", "Profit/Share", "Delta"]
    col_data = []
    for i in range(8):
        col_data.append([])
    for row in data:
        col_data[0].append(row.date)
        col_data[1].append(row.open)
        col_data[2].append(row.high)
        col_data[3].append(row.low)
        col_data[4].append(row.close)
        col_data[5].append(row.volume)
        col_data[6].append(row.pps)
        col_data[7].append(row.delta)

    df = {}
    for i in range(len(col_names)):
        df[col_names[i]] = col_data[i]
        
    df = pd.DataFrame(df, columns = col_names)
    df.to_csv(r"C:\Users\Dylan Pandjaris\Documents\Code\Value of Time\IBD\AMD_Processed.csv", index = False)
    
    print(df)
    

if __name__ == "__main__":
    export_csv()
    
    # UNCOMMENT BELOW 
    # for i in range(len(data)):
    #     add_day(i)
    
    # UNCOMMENT BELOW TO CLEAR DATA TABLE CONTENTS
    # delete_all()



