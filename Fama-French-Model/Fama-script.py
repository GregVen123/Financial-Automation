import numpy as np
import pandas as pd
from sklearn.linear_model import  LinearRegression

Fama = pd.read_csv("F-F_Research_Data_Factors_daily.CSV")
company_file = input("Input investing.com file name/location: ")
company = pd.read_csv(company_file)
company = company[::-1]
company["Close/Last"] =company["Close/Last"].replace("\$"," ",regex=True)
to_float = np.array(company["Close/Last"])
to_flaot2 = []
for i in to_float:
    to_flaot2.append(float(i))
company["Close/Last"] = to_flaot2
search = Fama[Fama["Date"] == 20150102]
#fix this
Fama = Fama.drop(index=range(0,23385))
New_mk = []
for i in range(len(Fama["Mkt-RF"])):
    New_mk.append(Fama.iloc[i]["Mkt-RF"]/100)
Fama["Mkt-RF"] = New_mk

new_smb = []
for i in range(len(Fama["SMB"])):
    new_smb.append(Fama.iloc[i]["SMB"]/100)
Fama["SMB"] = new_smb

new_hml = []
for i in range(len(Fama["HML"])):
    new_hml.append(Fama.iloc[i]["HML"]/100)
Fama["HML"] = new_hml


print(Fama)
company = company.drop(index=range(0,33))
#print(msft, Fama)
def percent_change(prev, forw):
    return (forw/prev)-1
cm_daily_change = [0]
for i in range(len(company)-1):
    cm_daily_change.append(percent_change(company.iloc[i]["Close/Last"], company.iloc[i+1]["Close/Last"]))

cm_daily_change = np.array(cm_daily_change)
cm_daily_change = np.around(cm_daily_change,5)
reg = LinearRegression()
#Xpart = np.array(Fama["Mkt-RF"])
#Xpart = Xpart.reshape(-1,1)

Xpart = Fama[["Mkt-RF","SMB","HML"]]
Ypart= cm_daily_change
reg.fit(Xpart,Ypart)
company["Percent Change"] = cm_daily_change
print(f'The Betas are in order of Market, SMB, MHL {reg.coef_}')

print(f' The intercept is {reg.intercept_}')
res = (min(company["Percent Change"]))

