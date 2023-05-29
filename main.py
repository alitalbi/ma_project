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
start_date = st.date_input("Start date:", pd.to_datetime("2018-01-01"))
end_date = st.date_input("End date:", pd.to_datetime(datetime.now().strftime("%Y-%m-%d")))


# Download the data and plot the close price
if search_term:
    data = download.data(search_term, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"),period="1d")

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.1)

    # Add subplot for price
    fig.add_trace(
        go.Scatter(x=data.index.to_list(), y=data.Price, name=search_term + " Close Price", mode="lines",
                   line=dict(width=2)),
        row=1, col=1
    )

    # Add subplot for volumes
    fig.add_trace(
        go.Scatter(x=data.index.to_list(), y=data.Volume, name=search_term + " Volume", mode="lines",
                   line=dict(width=2)),
        row=2, col=1
    )

    fig.update_layout(height=700, width=800, title_text="Price and Volume")
    st.plotly_chart(fig, use_container_width=True)