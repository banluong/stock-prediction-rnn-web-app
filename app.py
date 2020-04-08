from flask import Flask, render_template
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import datetime
from lstm import build_model
import plotly

app = Flask(__name__)


@app.route('/')
def home(name=None):
    return render_template("home.html", name=name)


@app.route('/about/')
def about(name=None):
    return render_template("about.html", name=name)


ticker_symbol = 'NFLX'
today = datetime.date.today()


def get_data(symbol, period, end_date):

    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    ticker_data = yf.Ticker(symbol)
    start_date = datetime.datetime(end_date.year-5, end_date.month, end_date.day)
    tickerDf = ticker_data.history(period=period, start=start_date, end=end_date)

    return tickerDf[columns]


def full_plot(y_inv, ytest_inv, ypred_inv):
    plt.plot(np.arange(0, len(y_inv)), y_inv, 'g', label="history")
    plt.plot(np.arange(len(y_inv), len(y_inv) + len(ytest_inv)), ypred_inv, 'r', label="prediction")
    plt.ylabel('Value')
    plt.xlabel('Time Step')
    plt.legend()
    plt.show()

    return plt


if __name__ == "__main__":
    app.run(debug=True)
