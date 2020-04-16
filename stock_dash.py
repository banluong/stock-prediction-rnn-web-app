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

options=[
    {'label': 'Netflix', 'value': 'NFLX'},
    {'label': 'Tesla', 'value': 'TSLA'},
    {'label': 'Google', 'value': 'GOOGL'}
]

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

    html.H3('Enter a stock symbol:', style={'paddingRight': '30px'}),
	dcc.Dropdown(
		id='my_ticker_symbol',
		options = options,
		value = ['TSLA'],
		multi = True
		# style={'fontSize': 24, 'width': 75}
		),

    html.Div([html.H3('Enter start / end date:'),
	dcc.DatePickerRange(id='my_date_picker',
						min_date_allowed = datetime.datetime(2015,1,1),
						max_date_allowed = datetime.date.today(),
						start_date = datetime.datetime(2019, 1, 1),
						end_date = datetime.date.today()
	)

], style={'display':'inline-block'}),
	html.Div([
		html.Button(id='submit-button',
					n_clicks = 0,
					children = 'Submit',
					style = {'fontSize': 24, 'marginLeft': '30px'}

		)

	], style={'display': 'inline-block'}),
    # Plotly stock graph
    dcc.Graph(
        id='graph-with-slider',
        figure=figure
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
