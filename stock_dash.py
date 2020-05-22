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
        children='Stock Price Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Stock price chart web application framework for Python.', style={
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
    # Date Range
    html.Div([html.H3('Enter start / end date:'),
              dcc.DatePickerRange(
                  id='date_range',
                  #start_date_placeholder_text='Start Date',
                  min_date_allowed=datetime(2015, 1, 1),
                  max_date_allowed=datetime.now(),
                  start_date=datetime(2019, 1, 1),
                  end_date=datetime.now(),
                  number_of_months_shown=2
    )

    ], style={'display': 'inline-block', 'color': colors['text']}),
    # Submit Button
    html.Div([
        html.Button(id='submit_button',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize': 18, 'marginLeft': '30px', 'backgroundColor': colors['text']}

                    )

    ], style={'display': 'inline-block'}),
    # Plotly stock graph
    dcc.Graph(
        id='graph_scatter'
    ),
    dcc.Graph(
        id='graph_candle'
    ),
    dcc.Graph(
        id='graph_volume'
    )
])

# app callback to update stock closing values


@app.callback(
    Output('graph_scatter', 'figure'),
    [Input('dropdown_symbol', 'value'),
     Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('submit_button', 'n_clicks')])
def update_scatter(symbol, start_date, end_date, n_clicks):
    if n_clicks == 0:
        ticker_data = yf.Ticker('TSLA')
        df = ticker_data.history(period='1d', start=datetime(2015, 1, 1), end=datetime.now())

    else:
        ticker_data = yf.Ticker(symbol)
        df = ticker_data.history(period='1d', start=start_date, end=end_date)

    first = go.Scatter(x=df.index,
                       y=df['Close'])

    data = [first]

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


# app callback to update candlestick stock values
@app.callback(
    Output('graph_candle', 'figure'),
    [Input('dropdown_symbol', 'value'),
     Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('submit_button', 'n_clicks')])
def update_graph(symbol, start_date, end_date, n_clicks):
    if n_clicks == 0:
        ticker_data = yf.Ticker('TSLA')
        df = ticker_data.history(period='1d', start=datetime(2015, 1, 1), end=datetime.now())

    else:
        ticker_data = yf.Ticker(symbol)
        df = ticker_data.history(period='1d', start=start_date, end=end_date)

    first = go.Candlestick(x=df.index,
                           open=df['Open'],
                           high=df['High'],
                           low=df['Low'],
                           close=df['Close'])

    data = [first]

    figure = {'data': data,
              'layout': {
                  'title': str(symbol) + " candlestick chart",
                  'plot_bgcolor': colors['background'],
                  'paper_bgcolor': colors['background'],
                  'font': {
                      'color': colors['text'],
                      'size': 18
                  }}
              }
    return figure

# Visual of stock volume


@app.callback(
    Output('graph_volume', 'figure'),
    [Input('dropdown_symbol', 'value'),
     Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('submit_button', 'n_clicks')])
def update_scatter(symbol, start_date, end_date, n_clicks):
    if n_clicks == 0:
        ticker_data = yf.Ticker('TSLA')
        df = ticker_data.history(period='1d', start=datetime(2015, 1, 1), end=datetime.now())

    else:
        ticker_data = yf.Ticker(symbol)
        df = ticker_data.history(period='1d', start=start_date, end=end_date)

    first = go.Scatter(x=df.index,
                       y=df['Volume'])

    data = [first]

    figure = {'data': data,
              'layout': {
                  'title': str(symbol) + " trading volume",
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
