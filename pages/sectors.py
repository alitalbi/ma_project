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
    sectors = pd.read_csv("https://raw.githubusercontent.com/alitalbi/ma_project/master/ISIN_sectors_ma.csv")
    sectors.drop("Unnamed: 0", axis=1, inplace=True)

    error_http_request = []
    stocks_dict = {}
    market_cap = pd.read_csv("https://raw.githubusercontent.com/alitalbi/ma_project/master/stocks_cap_info.csv")[
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
        df_stocks.loc[df_stocks['Instrument'] == company_name, '7d_return'] = return_value["7d_return"]
        df_stocks.loc[df_stocks['Instrument'] == company_name, '30d_return'] = return_value["30d_return"]

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
hover_options = ['Last day chg', '7d_return', '30d_return']
selected_hover_option = st.selectbox('Select Hover Option', hover_options)

hover_label = selected_hover_option
if selected_hover_option == '7d_return':
    hover_label = '7d_return'
elif selected_hover_option == '30d_return':
    hover_label = '30d_return'
fig = px.treemap(df_stocks, path=[px.Constant("all"), 'Sector', 'Instrument'], values='Market Cap', color='colors',
                 color_discrete_map={'(?)': '#262931', 'red': 'red', 'indianred': 'indianred',
                                     'lightpink': 'lightpink', 'lightgreen': 'lightgreen', 'lime': 'lime',
                                     'green': 'green'},
                 hover_data={hover_label: ':.2p'})
# Adjust the size of the figure
fig.update_layout(width=720, height=650)
st.plotly_chart(fig,use_container_width = False)



