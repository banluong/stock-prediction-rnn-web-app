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

tickerSymbol = 'NFLX'
today = datetime.date.today()

def get_data(symbol, period, endDate):

    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    tickerData = yf.Ticker(symbol)
    startDate = datetime.datetime(endDate.year-5,endDate.month,endDate.day)
    tickerDf = tickerData.history(period=period, start=startDate, end=endDate)

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
