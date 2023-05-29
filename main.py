from ma_fi import download
import streamlit as st
import pandas as pd
import yfinance as yf
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

#sys.path.insert(1, '/Users/talbi/PycharmProjects/streamLit/venv/lib/python3.10/site-packages')
st.set_page_config(page_title="Morrocan Stocks Exchange",page_icon="📈")



print(download.available_names)
a = download.data("ATTIJARIWAFA BANK","2018-01-01",'2022-01-01','1d')
a.set_index("Timestamp",inplace=True,drop=True)

# Set title and description of the app
st.title("Morrocan Stock Exchange ")
st.write("Talbi & Co Eco Framework (not ESG complaint) ")
st.sidebar.header("Analysis")
# Set up the search bar and date inputs
search_term = st.text_input("Enter a ticker (e.g. CIH):")
start_date = st.date_input("Start date:", pd.Timestamp("2019-01-01"))
end_date = st.date_input("End date:", pd.Timestamp(datetime.now().strftime("%Y-%m-%d")))
print(start_date)

# Download the data and plot the close price
if search_term:
    data = download.data(search_term, start_date, end_date,period="1d")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index.to_list(), y=data.Price,
                          name=search_term+ " Close Price",
                          mode="lines", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=data.index.to_list(), y=data.Volume,
                             name=search_term + "Volume",
                             mode="lines", line=dict(width=2)))
    st.plotly_chart(fig, use_container_width=True)