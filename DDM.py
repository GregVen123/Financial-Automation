import json

import pandas as pd
import numpy as np
from openpyxl import *
import datetime
import requests

#financial statements will be used in an updated version, the DDM does not use lines 11-53, starts at line 54
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
for i in range(len(length_test)-2): #replacing column headers with the year
    is_cols.append(str(2024-k))
    k+=1
is_cols.insert(0,"Income Statement") #first two column headers should be this
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
#cost of equity
def CAPM(risk_free_rate, beta,market_rate):
        return (risk_free_rate + (beta*(market_rate-risk_free_rate)))

try:
    market_rate = float(input("What is your preferred market rate (in decimal form e.g .08)?: "))
    risk_free_rate = float(input("What is the risk free rate in decimal form?: "))
    beta = float(input("What is the stock Beta?: "))
except:
        print("Not a valid int")

cost_of_equity = CAPM(risk_free_rate,beta,market_rate)

print(f"the cost of equity is {cost_of_equity}")
#user inputs type of DDM
#try:
#    stages = (int(input("Will the DDM be 1 or 2 stage (enter either 1 or 2 ): ")))
#except:
#        print('ERROR: ENTER EITHER 1 or 2 IN NUMBER FORM')

#Setting up the DDM
dividend_2024 = float(input("This year's dividend is? : "))
stage_1_rate = float(input("Stage 1 growth rate (decimal form): "))
stage_2_rate = float(input("Stage 2 growth rate (decimal form): "))
total_years = int(input("How many years is your model?: "))
years =[]
for i in range(total_years +1): #creating years plus 1 since DDM requires next dividend
    years.append(i)
dividends = [dividend_2024]
for i in range(total_years): #this creates an array of future dividends based on stage 1 growth rate
    dividends.append(dividend_2024*(1+stage_1_rate)**(i+1))

dividends = np.around(dividends,3)
def present_value(fv,r,n):
    return(round(float(fv/((1+r)**n)),3))

pv_dividends =[] #gets the present value of the stage 1 dividends
for i in range(len(dividends)):
    pv_dividends.append(present_value(dividends[i],cost_of_equity,years[i]))

print(pv_dividends)
stage_1_pv = sum(pv_dividends[1:])
stage_2_value = (dividends[max(years)]*(1+stage_2_rate)/(cost_of_equity-stage_2_rate))
stage_2_pv =present_value(stage_2_value,cost_of_equity,max(years))
intrinsic_value = stage_1_pv+stage_2_pv
print(intrinsic_value)
#url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=DRI&apikey=VGMETC1M5S3ME3AH"
#r = requests.get(url)

#print(r.status_code)

#data = r.json()
#data2 = (data["Monthly Time Series"])
#df = pd.DataFrame(data2)
#alpha = df.loc["4. close"]
#print(alpha)

#urd = "https://www.alphavantage.co/query?function=DIVIDENDS&symbol=DRI&apikey=VGMETC1M5S3ME3AH"
#rd = requests.get(urd)
#div_data = rd.json()

#div_data_df = pd.DataFrame(div_data["data"])

#div_data_df = div_data_df.drop(["declaration_date","record_date","payment_date"],axis=1)
#print(div_data_df)
#dividend_amount_Q = []
#dividend_amount_Y = []
#for i in div_data_df["amount"]:
#    dividend_amount_Q.append(i)
#qtr_dividend = np.array(dividend_amount_Q, dtype="float")
#put quarterly data into years
#for i in range(0,(len(qtr_dividend)//4)):
#    i*=4
#    dividend_amount_Y.append(qtr_dividend[i]+qtr_dividend[i+1]+qtr_dividend[i+2]+qtr_dividend[i+3])

#print(dividend_amount_Y)

