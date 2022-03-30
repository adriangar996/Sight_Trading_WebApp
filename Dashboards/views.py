from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser
from Dashboards.models import Theme
import requests
import json




#Extracting NASDAQ data for Dashboard Index (NASDAQ(^IXIC) Prev.close, Day Range, Year Range)
@login_required
def indexView(request):
    user_id = request.user.id
    user = PortfolioUser.objects.filter(user=user_id)[0]

    #Get users theme
    theme_user = Theme.objects.filter(user=user)

    url = "https://yfapi.net/v6/finance/quote"

    querystring = {"symbols":"^IXIC"}

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
      'year_range' : year_range,
      'theme_user' : theme_user
    }

    return render(request, 'dashboardindex.html', context)  



