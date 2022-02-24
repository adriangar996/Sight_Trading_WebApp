from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser
from yahoo_finance import Share
import requests
import json





@login_required
def indexView(request):

    url = "https://yfapi.net/v6/finance/quote"

    querystring = {"symbols":"NDAQ"}

    headers = {
    'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"
    }

    r = requests.request("GET", url, headers=headers, params=querystring)
    data = r.json()

    response = data['quoteResponse']
    result = response['result']

    for i in result:

        prev_close = i['regularMarketPreviousClose']
        day_range = i['regularMarketDayRange']
        year_range = i['fiftyTwoWeekRange']

    context={
      'prev_close' : prev_close,
      'day_range' : day_range,
      'year_range' : year_range
    }

    return render(request, 'dashboardindex.html', context)  




#  url = "https://yfapi.net/v6/finance/quote"

#     querystring = {"symbols":"NDAQ"}

#     headers = {
#     'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"
#     }

#     r = requests.request("GET", url, headers=headers, params=querystring)
#     data = r.json()

#     context={
#       'data' : data,
#     }



#   index = Share('NDAQ')

#     prev_close = index.get_prev_close()
#     day_high = index.get_days_high()
#     day_low = index.get_days_low()
#     year_high = index.get_year_high()
#     year_low = index.get_year_low()

#     context={
#         'prev_close' : prev_close,
#         'day_high' : day_high,
#         'day_low' : day_low,
#         'year_high' : year_high,
#         'year_low' : year_low,
#     }