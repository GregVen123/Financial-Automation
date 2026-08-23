import pandas as pd
import requests
import numpy as np
import plotly.express as px
import pypfopt
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

def pull_stock_data():
    try:
        num_stocks = int(input("How many stocks are you analyzing?: "))
    except ValueError:
        print("Not a valid integer.")
        return None

    close_columns = []

    for i in range(num_stocks):
        ticker = input("Enter stock ticker: ").strip().upper()
        url = (
            "https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&apikey={API_KEY}"
        )
        r = requests.get(url)
        data = r.json()

        if "Weekly Adjusted Time Series" not in data:
            print(f"Problem with {ticker}: {data.get('Note') or data.get('Error Message') or data}")
            continue

        df = pd.DataFrame(data["Weekly Adjusted Time Series"]).T
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        # grab just the adjusted close column, rename it to the ticker
        close = df["5. adjusted close"].rename(ticker)
        close_columns.append(close)

    if not close_columns:
        print("No valid data pulled.")
        return None

    # combine on common dates only
    combined = pd.concat(close_columns, axis=1, join="inner")
    return combined

result = pull_stock_data()
percent_results = result.pct_change().dropna()

result.to_csv('output.csv', index =True)