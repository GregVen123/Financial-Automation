import json

import pandas as pd
import numpy as np
from openpyxl import *
import datetime
import requests

#putting data in dataframe
balance_sheet1 = pd.read_excel("AAPL Balance Sheet Statement (Annual) - Discounting Cash Flows.xlsx")
cash_flows_statement1 = pd.read_excel("AAPL Cash Flow Statement (Annual) - Discounting Cash Flows.xlsx")
income_statement1 = pd.read_excel("AAPL Income Statement (Annual) - Discounting Cash Flows.xlsx")
balance_sheet = balance_sheet1.replace(",","", regex=True)
income_statement = income_statement1.replace(",","",regex=True)
cash_flows_statement = cash_flows_statement1.replace(",","", regex=True)
bs_cols = []
cf_cols = []
is_cols = []
length_test = []
for i in income_statement.columns:
    length_test.append(i)
k = 1
for i in range(len(length_test)-2):
    is_cols.append(str(2024-k))
    k+=1
is_cols.insert(0,"Income Statement")
is_cols.insert(1,"TTM")

income_statement.columns = is_cols
k_2 =1
for i in range(len(length_test)-2):
    bs_cols.append(str(2024-k_2))
    k_2+=1
bs_cols.insert(0,"Balance Sheet")
balance_sheet.columns = bs_cols
cf_length = []
for i in cash_flows_statement.columns:
    cf_length.append(i)
k_3 =1
for i in range(len(cf_length)-2):
    cf_cols.append(str(2024-k_3))
    k_3+=1


cf_cols.insert(0,"Cash Flows Statement")
cf_cols.insert(1,"TTM")
income_statement = income_statement.drop(0)
cash_flows_statement.columns = cf_cols
#setting errors = "coerce" sets any erroe to NaN
#since column 1 are strings and the others are ints, the entire data in dataframe are strings so this converts them
for column in income_statement.columns[1:]:
    income_statement[column] = pd.to_numeric(income_statement[column], errors="coerce").astype("int")

def CAPM(risk_free_rate, beta,market_rate):
        return (risk_free_rate + (beta*(market_rate-risk_free_rate)))

try:
    market_rate = float(input("What is your preferred market rate (in decimal form e.g .08)?: "))
    risk_free_rate = float(input("What is the risk free rate in decimal form?: "))
    beta = float(input("What is the stock Beta?: "))
except:
        print("Not a valid int")

cost_of_equity = CAPM(risk_free_rate,beta,market_rate)

print(cost_of_equity)

try:
    stages = (int(input("Will the DDM be 1 or 2 stage (enter either 1 or 2 ): ")))
except:
        print('ERROR: ENTER EITHER 1 or 2 IN NUMBER FORM')


charlie = np.zeros((3,5))
print(charlie)

url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=DRI&apikey=DEMO"
r = requests.get(url)

print(r.status_code)

data = r.json()
df = pd.DataFrame(data)
print(df)

#delta = pd.DataFrame(data)
#print(delta)
