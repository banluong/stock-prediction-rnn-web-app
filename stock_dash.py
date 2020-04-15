# https://dash.plotly.com/layout
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import yfinance as yf
import plotly.graph_objects as go


app = dash.Dash()

symbol = "TSLA"

# candle_stick
ticker_data = yf.Ticker(symbol)
end_date = datetime.date.today()
start_date = datetime.datetime(end_date.year-1, end_date.month, end_date.day)
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

figure = go.Figure(data=data, layout=layout)

graph = dcc.Graph(
    id='graph-with-slider',
    figure=figure
)


colors = {
    'background': '#F5FFFA',
    'text': '#00FA9A'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'Netflix', 'value': 'NFLX'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Google', 'value': 'GOOGL'}
        ],
        value='GOOGL'
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'Netflix', 'value': 'NFLX'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Google', 'value': 'GOOGL'}
        ],
        value=['NFLX', 'TSLA'],
        multi=True
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'Netflix', 'value': 'NFLX'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Google', 'value': 'GOOGL'}
        ],
        value='TSLA'
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': 'Netflix', 'value': 'NFLX'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Google', 'value': 'GOOGL'}
        ],
        value=['NFLX', 'TSLA']
    ),

    html.Label('Text Input'),
    dcc.Input(value='TSLA', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),

    # Plotly stock graph
    graph
])

if __name__ == '__main__':
    app.run_server(debug=True)
