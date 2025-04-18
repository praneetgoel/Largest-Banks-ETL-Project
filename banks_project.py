# -*- coding: utf-8 -*-
"""banks_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16_CdepVCybl0G3c0hK1rXwAfoVj_XYdH
"""

# Importing the required libraries
import requests
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

# Code for ETL operations on Country-GDP data
def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open ("code_log.txt","a") as f:
        f.write(timestamp + ' : ' + message + '\n')

def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns = table_attribs)
    table = data.find_all('tbody')
    rows = table[0].find_all('tr')
    # print(rows[0:2])
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {
                "Name" : col[1].find_all('a')[1].get_text(strip = True),
                "MC_USD_Billion" : col[2].get_text(strip = True)}
            df1 = pd.DataFrame(data_dict, index = [0])
            df = pd.concat([df,df1], ignore_index = True)
    # print(df)
    return df

def transform(df, csv_path):
    df['MC_USD_Billion'] = df['MC_USD_Billion'].astype(float)
    exchange_rates = pd.read_csv('exchange_rate.csv')
    currency_dict = exchange_rates.set_index('Currency')['Rate'].to_dict()
    df['MC_GBP_Billion'] = np.round(df['MC_USD_Billion'] * currency_dict['GBP'],2)
    df['MC_EUR_Billion'] = np.round(df['MC_USD_Billion'] * currency_dict['EUR'],2)
    df['MC_INR_Billion'] = np.round(df['MC_USD_Billion'] * currency_dict['INR'],2)
    # print(df)
    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists = 'replace', index = False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["Name", "MC_USD_Billion"]
db_name = 'Banks.db'
table_name = 'Largest_banks'
# csv_path = './exchange_rate.csv'
csv_path = './Largest_banks_data.csv'
sql_connection = sqlite3.connect(db_name)

log_progress('Preliminaries complete. Initiating ETL process')
df = extract(url, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df,csv_path)

log_progress('Data transformation complete. Initiating loading process')
load_to_csv(df, csv_path)
log_progress('Data saved to CSV file')

log_progress('SQL Connection initiated.')
load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query')

query_statement = f"SELECT * from {table_name}"
run_query(query_statement, sql_connection)

query_statement = f"SELECT AVG(MC_GBP_Billion) from {table_name}"
run_query(query_statement, sql_connection)

query_statement = f"SELECT Name from {table_name} LIMIT 5"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')
sql_connection.close()

