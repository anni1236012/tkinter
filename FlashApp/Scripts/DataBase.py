# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 23:21:05 2021

@author: Vmaha
"""

import sqlite3 as sl

import pandas as pd

connection = sl.connect(r'C:\Users\Vmaha\FlashApp\DataBase\FlashApp.db')

connection.row_factory = sl.Row

loc_path = r'C:\Users\Vmaha\FlashApp\DataBase\Test.xlsx'

df = pd.read_excel(loc_path,engine ='openpyxl',index_col = 0)
df.to_sql('Test',connection)

cur = connection.cursor()
cur.execute('''select * from Test ''')
connection.close()