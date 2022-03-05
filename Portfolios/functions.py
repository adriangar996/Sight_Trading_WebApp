from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import yfinance
import plotly.graph_objects as go
from plotly.offline import plot

#Candlestick chart in portfolio
def candles1(choice1):
    symbol = choice1
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
            autosize = False,
            width = 1000,
            height = 680,
            paper_bgcolor="rgb(254,217,166)",
            plot_bgcolor = 'rgb(242,242,242)',
            title = {
                'text': '',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

    y_axis = figure.update_yaxes(
            title_text = 'Close Price',
            tickprefix = '$',
        )

    chart1 = plot(figure, output_type = 'div')
    return chart1

#Second chart in portfolio
# def candles2(choice2):
#     symbol = choice2
#     stock = yfinance.Ticker(symbol)
#     hist = stock.history(period='1y', interval='1d')
#     figure = go.Figure(data = [go.Candlestick(x =hist.index,
#                                                  open = hist['Open'],
#                                                  high = hist['High'],
#                                                  low = hist['Low'],
#                                                  close = hist['Close']
#                                             )
#                             ]
#                     )
#     x_axis = figure.update_xaxes(
#             title_text = 'Date',
#             rangeslider_visible = True,
#             rangeselector = dict(
#                 buttons = list([
#                     dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
#                     dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
#                     dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
#                     dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
#                     dict(step = 'all')
#                 ])
#             )
#         )

#     layout = figure.update_layout(
#             title = {
#                 'text': '',
#                 'y':0.9,
#                 'x':0.5,
#                 'xanchor': 'center',
#                 'yanchor': 'top'
#             }
#         )

#     y_axis = figure.update_yaxes(
#             title_text = 'Close Price',
#             tickprefix = '$'
#         )

#     chart2 = plot(figure, output_type = 'div')
#     return chart2

#Candlestick Chart for Watchlist
def candles3(choice1):
    symbol = choice1
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
            autosize = False,
            width = 1000,
            height = 680,
            paper_bgcolor="rgb(254,217,166)",
            plot_bgcolor = 'rgb(242,242,242)',
            title = {
                'text': '',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

    y_axis = figure.update_yaxes(
            title_text = 'Close Price',
            tickprefix = '$'
        )

    chart3 = plot(figure, output_type = 'div')
    return chart3

# def candles4(choice2):
#     symbol = choice2
#     stock = yfinance.Ticker(symbol)
#     hist = stock.history(period='1y', interval='1d')
#     figure = go.Figure(data = [go.Candlestick(x =hist.index,
#                                                  open = hist['Open'],
#                                                  high = hist['High'],
#                                                  low = hist['Low'],
#                                                  close = hist['Close']
#                                             )
#                             ]
#                     )
#     x_axis = figure.update_xaxes(
#             title_text = 'Date',
#             rangeslider_visible = True,
#             rangeselector = dict(
#                 buttons = list([
#                     dict(count = 1, label = '1M', step = 'month', stepmode = 'backward'),
#                     dict(count = 6, label = '6M', step = 'month', stepmode = 'backward'),
#                     dict(count = 1, label = 'YTD', step = 'year', stepmode = 'todate'),
#                     dict(count = 1, label = '1Y', step = 'year', stepmode = 'backward'),
#                     dict(step = 'all')
#                 ])
#             )
#         )

#     layout = figure.update_layout(
#             title = {
#                 'text': '',
#                 'y':0.9,
#                 'x':0.5,
#                 'xanchor': 'center',
#                 'yanchor': 'top'
#             }
#         )

#     y_axis = figure.update_yaxes(
#             title_text = 'Close Price',
#             tickprefix = '$'
#         )

#     chart4 = plot(figure, output_type = 'div')
#     return chart4