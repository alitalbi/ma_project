import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import urllib
from ma_fi import download
import os
@st.cache
def load_data():


    current_dir = os.path.abspath(os.path.dirname(__file__))
    sectors = pd.read_csv(os.path.join(current_dir, "ISIN_sectors_ma.csv"))
    sectors.drop("Unnamed: 0", axis=1, inplace=True)

    error_http_request = []
    stocks_dict = {}
    market_cap = pd.read_excel(os.path.join(current_dir, "stocks_cap_info.xlsx"), sheet_name="Sheet1")[
        ["Instrument", "Market Cap"]
    ]
    market_cap["Market Cap"] = market_cap["Market Cap"].apply(lambda x: int(x.replace("\xa0", "")))
    df_stocks = pd.merge(market_cap, sectors, on="Instrument")
    for elem in sectors.Instrument:
        stocks_dict[elem] = {
            'historical prices': "",
            'Last day chg': "",
            "7d_return": "",
            "30d_return": "",
            "1y_return": ""
        }
    start_date = "2018-01-01"
    end_date = pd.Timestamp.now().strftime("%Y-%m-%d")

    for elem in sectors.Instrument:
        try:
            data = download.data(elem, start_date, end_date, period="1d")[::-1]
            data.reset_index(inplace=True, drop=True)
            if len(data) > 0:
                stocks_dict[elem]['historical prices'] = data
                stocks_dict[elem]["Last day chg"] = data.Price.pct_change(1)[1]
                stocks_dict[elem]["7d_return"] = data.Price.pct_change(7)[7]
                stocks_dict[elem]["30d_return"] = data.Price.pct_change(22)[22]
        except urllib.error.HTTPError:
            error_http_request.append(elem)

    for elem in error_http_request:
        stocks_dict.pop(elem)

    for company_name, return_value in stocks_dict.items():
        df_stocks.loc[df_stocks['Instrument'] == company_name, 'Last day chg'] = return_value["Last day chg"]

    # Convert 'Last day chg' column to numeric
    df_stocks['Last day chg'] = pd.to_numeric(df_stocks['Last day chg'], errors='coerce')

    # Remove rows with missing or invalid values in the 'Last day chg' column
    df_stocks = df_stocks.dropna(subset=['Last day chg']).copy()

    # Perform the cut operation on the cleaned DataFrame
    color_bin = [-1, -0.02, -0.01, 0, 0.01, 0.02, 1]
    df_stocks['colors'] = pd.cut(df_stocks['Last day chg'], bins=color_bin,
                                 labels=['red', 'indianred', 'lightpink', 'lightgreen', 'lime', 'green'])

    return df_stocks


st.title("Sector Screening")

df_stocks = load_data()

fig = px.treemap(df_stocks, path=[px.Constant("all"), 'Sector', 'Instrument'], values='Market Cap', color='colors',
                 color_discrete_map={'(?)': '#262931', 'red': 'red', 'indianred': 'indianred',
                                     'lightpink': 'lightpink', 'lightgreen': 'lightgreen', 'lime': 'lime',
                                     'green': 'green'},
                 hover_data={'Last day chg': ':.2p'})

st.plotly_chart(fig)



