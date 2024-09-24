import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


dfsp0 = pd.read_csv("Download Data - INDEX_US_S&P US_SPX (1).csv")
dftr0 = pd.read_csv("daily-treasury-rates.csv")

#since data is from end of year to beginning of year doing iloc[::-1] reverses the index so it starts bottom up
#[::-1] first colon reps start stop, second colon reps step, -1 indicates to go in reverse index
dfsp = dfsp0.iloc[::-1]
dftr = dftr0.iloc[::-1]

def daily_change(num1,num2):
    try:
        return round(((num2-num1)/num1)*100,2)
    except ZeroDivisionError:
        return 0

list1 = dfsp["Close"].tolist()
spclosea = []
for i in list1:
    spclosea.append(i.replace(",",""))
spclose = [0]
for i in spclosea:
    spclose.append(float(i))
print(spclose)
spcloseb = []
for i in spclosea:
    spcloseb.append(float(i))
SP_Change = []
for i in range(len(spclose)-1):
    k = i+1
    SP_Change.append(daily_change(spclose[i],spclose[k]))

print(spclose)
print(SP_Change)
dfsp.insert(5,"Change",SP_Change)

list2 = dftr["1 Yr"].tolist()

Tr_Change = [0]
for i in range(len(list2) -1):
    k = i +1
    Tr_Change.append(daily_change(list2[i],list2[k]))

dftr.insert(14,"Change",Tr_Change)

day = []
for i in range(len(list2)):
    day.append(i)

sp_tr = {
    "Day": day,
    "SP500 Value": spcloseb,
    "Treasury Rates": dftr["1 Yr"],
    "SP % Change": dfsp.Change,
    "Treasury % Change": dftr.Change

}

df3 = pd.DataFrame(sp_tr)
#print(df3)
#fig = px.line(df3, x="Day", y="Treasury Rates", title="Treasury Rates 2023 Graph")
#fig.add_scatter(x=df3["Day"],y=df3["SP500 Value"])
#fig.show()
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=sp_tr["Day"], y=sp_tr["SP500 Value"],name="SP500 Price"), secondary_y=False)
fig.add_trace(go.Scatter(x=sp_tr["Day"],y=sp_tr["Treasury Rates"], name="Treasury Rate"), secondary_y=True)

fig.show()

#next make a choice between different treasury notes
