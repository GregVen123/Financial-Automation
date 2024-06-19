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
income_statement["2023"].astype("float")
income_statement["2022"].astype("float")

alpha= income_statement.loc[(income_statement["2023"] == 0) & (income_statement["2022"] == 0)]
print(alpha)
#balance, cash, income
#C:\Users\kingo\PycharmProjects\Valuation_Project\AAPL Balance Sheet Statement (Annual) - Discounting Cash Flows.xlsx
#C:\Users\kingo\PycharmProjects\Valuation_Project\AAPL Cash Flow Statement (Annual) - Discounting Cash Flows.xlsx
#C:\Users\kingo\PycharmProjects\Valuation_Project\AAPL Income Statement (Annual) - Discounting Cash Flows.xlsx
