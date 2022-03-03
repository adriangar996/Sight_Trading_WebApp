from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import yfinance
import plotly.graph_objects as go
from plotly.offline import plot

def candles():
    symbol = 'AAPL'
    stock = yfinance.Ticker(symbol)
    hist = stock.history(period='1y', interval='1d')
    figure = go.Figure(data = [go.Candlestick(x =hist.index,
                                                 open = hist['Open'],
                                                 high = hist['High'],
                                                 low = hist['Low'],
                                                 close = hist['Close']
                                            )
                            ]
                    )
    x_axis = figure.update_xaxes(
            title_text = 'Date',
            rangeslider_visible = True,
            rangeselector = dict(
                buttons = list([
                    dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
                    dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
                    dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
                    dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
                    dict(step = 'all')
                ])
            )
        )

    layout = figure.update_layout(
            title = {
                'text': 'AMZN',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

    y_axis = figure.update_yaxes(
            title_text = 'AMZN Close Price',
            tickprefix = '$'
        )

    chart = plot(figure, x_axis, layout, y_axis, output_type = 'div')
    return chart