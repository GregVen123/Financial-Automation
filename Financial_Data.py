import pandas as pd

df1 = pd.read_csv("output1.csv")
df2 = pd.read_csv("output2.csv")
df3 = pd.read_csv("output3.csv")

df3 = df3.replace("—",0)
df2 = df2.replace("—",0)
df1 = df1.replace("—",0)

df1.to_excel("test1.xlsx")
df2.to_excel("test2.xlsx")
df3.to_excel("test3.xlsx")

#print(df4)



#replace commas and Nan



