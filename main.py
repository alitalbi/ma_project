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

start_date = st.date_input("Start date:", pd.to_datetime("2018-01-01"))
end_date = st.date_input("End date:", pd.to_datetime(datetime.now().strftime("%Y-%m-%d")))

search_terms = st.text_input("Enter tickers separated by comma (e.g. CIH, ATTIJARIWAFA BANK):")
search_terms = [term.strip() for term in search_terms.split(",")]

# Download the data and plot the close price
if search_terms:
    # Create a figure for the prices
    fig_prices = go.Figure()

    # Create a figure for the volumes
    fig_volumes = go.Figure()
    for term in search_terms:
        # Get data for the search term
        data = download.data(term, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), period="1d")
        data.set_index("Timestamp",inplace=True,drop=True)
        # Add trace for prices
        fig_prices.add_trace(go.Scatter(x=data.index.to_list(), y=data.Price,
                                        name=term + " Close Price",
                                        mode="lines", line=dict(width=2)))

        # Add trace for volumes
        fig_volumes.add_trace(go.Scatter(x=data.index.to_list(), y=data.Volume,
                                         name=term + " Volume",
                                         mode="lines", line=dict(width=2)))

            # Plot the prices and volumes in the same graph
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.05,
                        subplot_titles=["Close Prices", "Volumes"])

    # Add the traces from the price figure to the combined graph
    for trace in fig_prices.data:
        fig.add_trace(trace, row=1, col=1)

    # Add the traces from the volume figure to the combined graph
    for trace in fig_volumes.data:
        fig.add_trace(trace, row=2, col=1)

    # Update layout
    fig.update_layout(height=800, width=800, title_text="Price and Volume")

    # Plot the combined graph
    st.plotly_chart(fig, use_container_width=True)