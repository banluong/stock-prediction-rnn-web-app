import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
import yfinance as yf
from fbprophet import Prophet
import plotly.graph_objects as go


app = dash.Dash()

options = [
    {'label': 'Apple', 'value': 'AAPL'},
    {'label': 'Facebook', 'value': 'FB'},
    {'label': 'Google', 'value': 'GOOGL'},
    {'label': 'IBM', 'value': 'IBM'},
    {'label': 'Microsoft', 'value': 'MSFT'},
    {'label': 'Netflix', 'value': 'NFLX'},
    {'label': 'Tesla', 'value': 'TSLA'}
]

colors = {
    'background': '#191414',
    'text': '#1DB954'
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'font-family': "Helvetica"}, children=[
    html.H1(
        children='Stock Forecast Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Stock price forecasting chart web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    # Ticker Symbol Dropdown
    html.H3('Enter a stock symbol:', style={'paddingRight': '30px', 'color': colors['text']}),
    dcc.Dropdown(
        id='dropdown_symbol',
        options=options,
        value='TSLA',
        multi=False
    ),
    # Submit Button
    html.Div([
        html.Button(id='submit_button',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize': 18, 'marginLeft': '625px', 'backgroundColor': colors['text']}

                    )

    ], style={'display': 'inline-block'}),
    # Plotly stock graph
    dcc.Graph(
        id='graph_scatter'
    )
])

# app callback to update stock closing values


@app.callback(
    Output('graph_scatter', 'figure'),
    [Input('dropdown_symbol', 'value'),
     Input('submit_button', 'n_clicks')])
def update_scatter(symbol, n_clicks):
    if n_clicks == 0:
        ticker_data = yf.Ticker('TSLA')
        df = ticker_data.history(period='1d', start=datetime(2015, 1, 1), end=datetime.now())

    else:
        #columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        ticker_data = yf.Ticker(symbol)
        df = ticker_data.history(period='1d', start=datetime(2015, 1, 1), end=datetime.now())

    prophet_df = df.copy()
    prophet_df.reset_index(inplace=True)
    # Renaming needed for fbprophet to make predictions
    prophet_df = prophet_df.rename(columns={"Date": "ds", "Close": "y"})

    # Call Prophet() to make prediction up to 100 days
    forcast_columns = ['yhat', 'yhat_lower', 'yhat_upper']
    m = Prophet()
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=100)
    forecast = m.predict(future)
    forecast = forecast.rename(columns={"ds": "Date"})
    forecast1 = forecast.set_index("Date")
    forecast1 = forecast1[datetime.now():]

    historic = go.Scatter(
        x=df.index,
        y=df["Close"],
        name="Data values"
    )

    yhat = go.Scatter(
        x=forecast1.index,
        y=forecast1["yhat"],
        mode='lines',
        name="Forecast"
    )

    yhat_upper = go.Scatter(
        x=forecast1.index,
        y=forecast1["yhat_upper"],
        mode='lines',
        fill="tonexty",
        line={"color": "#57b8ff"},
        name="Higher uncertainty interval"
    )

    yhat_lower = go.Scatter(
        x=forecast1.index,
        y=forecast1["yhat_lower"],
        mode='lines',
        fill="tonexty",
        line={"color": "#57b8ff"},
        name="Lower uncertainty interval"
    )

    data = [historic, yhat, yhat_upper, yhat_lower]

    figure = {'data': data,
              'layout': {
                  'title': str(symbol) + " closing value",
                  'plot_bgcolor': colors['background'],
                  'paper_bgcolor': colors['background'],
                  'font': {
                      'color': colors['text'],
                      'size': 18
                  }}
              }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
