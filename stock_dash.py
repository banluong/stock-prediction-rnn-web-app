import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
import yfinance as yf
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

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
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
        # style={'fontSize': 24, 'width': 75}
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
        id='graph_candle'
    ),
])

# app callback to update graph


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

    layout = go.Layout(title={
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

    figure = {'data': data, 'layout': layout}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
