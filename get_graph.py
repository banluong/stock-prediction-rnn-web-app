"""
LSTM RNN model

created by: Ban Luong
"""
import yfinance as yf
import pandas as pd
import plotly
import datetime
import plotly.graph_objects as go
import plotly.offline as po
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.figsize'] = (16, 10)
mpl.rcParams['axes.grid'] = False


def candle_stick(symbol, end_date):
    ticker_data = yf.Ticker(symbol)
    start_date = datetime.datetime(end_date.year-5, end_date.month, end_date.day)
    df = ticker_data.history(period='1d', start=start_date, end=end_date)

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.update_layout(
        title={
            'text': symbol,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Times New Roman",
            size=20,
            color="#7f7f7f"
        )
    )

    po.plot(fig, filename='templates/dashboard.html',auto_open=False)
