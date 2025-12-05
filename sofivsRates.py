import numpy as np
import pandas as pd
import plotly.express as px
from openpyxl import *
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


wb = load_workbook('Polymarket Rate Data.xlsx')
ws = wb['Final']
data = ws.values
df = pd.DataFrame(data)
expected_values = list(df.iloc[:,1])

def percent_change(value1,value2):
    return (((value2)-(value1))/(abs(value1)))*100

expected_value_change = [0]
for i in range(len(expected_values)-1):
    expected_value_change.append(percent_change(expected_values[i],expected_values[i+1]))


df['Change'] = expected_value_change
sofiDF = pd.read_csv('SoFi5Y.csv')
dfrates = pd.read_csv('DGS1.csv')
sofiDF = sofiDF.iloc[::-1]
df.rename(columns={0:'Date',1:'Expected Value','Change':'Change'}, inplace=True)
sofiDF.rename(columns={'Change %': 'Stock Change %'},inplace=True)
mergeddf = pd.merge(df,sofiDF,'right','Date')
mergeddf.drop(['Open','High','Low','Vol.'],axis=1,inplace=True)
print(dfrates)
reg_data = mergeddf.iloc[27:]
reg_data = reg_data[reg_data['Change'] >= -80]
reg_data['Stock Change %'] = reg_data['Stock Change %'].str.rstrip('%').astype(float)
X = reg_data[['Change']]
Y = reg_data[['Stock Change %']]
model = LinearRegression()
model.fit(X,Y)

print(model.coef_)
print(model.intercept_)

# Scatter plot with linear regression line
fig = px.scatter(
    reg_data,
    x='Change',        
    y='Stock Change %',        
    trendline='ols',     
    title='Linear Regression Scatter Plot'
)

#fig.show()
X_sm = sm.add_constant(X)
model_sm = sm.OLS(Y, X_sm).fit()

#print(model_sm.summary())

#**COMPARING TREASURY RATES WITH SOFI STOCK**
mergeddf2 = pd.merge(sofiDF,dfrates,'left','Date')
mergeddf2 = mergeddf2.dropna(subset=['DGS1'])
mergeddf2.drop(['Open','High','Low','Vol.'],axis=1,inplace=True)
mergeddf2['Stock Change %'] = mergeddf2['Stock Change %'].str.rstrip('%').astype(float)
mergeddf2 = mergeddf2[mergeddf2['Stock Change %'] <= 17]

treasuryvssofi = mergeddf2.iloc[27:]
treasuryvssofi.reset_index(drop=True)
expected_rate_change = [0]
for i in range(len(treasuryvssofi)-1):
    expected_rate_change.append(percent_change(treasuryvssofi['DGS1'].iloc[i],treasuryvssofi['DGS1'].iloc[i+1]))
treasuryvssofi['Rate Change %'] = expected_rate_change

fig2 = px.scatter(
    treasuryvssofi,
    x='Rate Change %',        
    y='Stock Change %',        
    trendline='ols',     
    title='SoFi Stock Daily $ Change vs 1 Year Treasury Daily % Change'
)
fig2.show()
x2 = treasuryvssofi['Rate Change %']
y2 = treasuryvssofi['Stock Change %']
X_sm2 = sm.add_constant(x2)
model_sm2 = sm.OLS(y2, X_sm2).fit()

print(model_sm2.summary())

#**SAME THING BUT ELIMINATING NO CHANGES**
# treasuryvssofi2 = treasuryvssofi[treasuryvssofi['Rate Change %'] != 0]

# x3 = treasuryvssofi2['Rate Change %']
# y3 = treasuryvssofi2['Stock Change %']
# X_sm3 = sm.add_constant(x3)
# model_sm3 = sm.OLS(y3, X_sm3).fit()
# fig3 = px.scatter(
#     treasuryvssofi2,
#     x='Rate Change %',        
#     y='Stock Change %',        
#     trendline='ols',     
#     title='Linear Regression Scatter Plot'
# )
# fig3.show()
# print(model_sm3.summary())
