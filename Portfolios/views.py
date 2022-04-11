from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from Portfolios.models import StockPortfolio, PortfolioUser
from Portfolios.models import Watchlist
import time
import decimal
from .forms import AddStockForm, AddWatchlistForm
from .functions import *
import logging
import requests
from django.contrib import messages
from Dashboards.models import Predictions
from Dashboards.models import Theme
from Dashboards.models import Notifications
from django.views.decorators.csrf import csrf_exempt


# CREATING LOGGER
logger = logging.getLogger('LOG')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

@csrf_exempt
@login_required
def portfolioView(request):

    #Get user id
    user_id = request.user.id
    user = PortfolioUser.objects.filter(user=user_id)[0]

    #Filter portfolio stocks by user
    stock_list = StockPortfolio.objects.filter(user_id=user)

    #Get today's date
    today_date = time.strftime("%m.%d.%Y")

    #Get stock the user selected from dropdown for loading to chart1 and chart2
    if request.method == 'POST':
        choice1 = request.POST.get('stock_selected1', '')
    else:
        choice1 = ''  

    #Getting and plotting data from functions.py to render in portfolio.html
    candlestick1 = candles1(choice1)

    #Get current price and percent change from database for chart with user symbol choice 
    chart_values1 = StockPortfolio.objects.filter(user=user, symbol=choice1)

    #Get predictions from DB
    pred_list = Predictions.objects.filter(symbol=choice1)

    #Get users theme
    theme_user = Theme.objects.filter(user=user)

    #Get stock to be added to portfolio from user
    if 'add_stock' in request.POST:

            form = AddStockForm(request.POST)

            if form.is_valid():  # form validation
                new_stock = request.POST.get("add_stock", "")

                if not StockPortfolio.objects.filter(user=user, symbol=new_stock.upper()):  # stock not already in portfolio

                    logger.info('Adding ' + new_stock.upper() + ' to stock portfolio')

                    try:  # try to add stock to portfolio
                        url = "https://yfapi.net/v6/finance/quote"

                        querystring = {"symbols":new_stock.upper()}

                        headers = {
                        'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"  
                        }

                        r = requests.request("GET", url, headers=headers, params=querystring)
                        data = r.json()

                        response = data['quoteResponse']
                        result = response['result']

                        #Get data from JSON file
                        for i in result:

                            new_stock_price = i['regularMarketPrice']
                            new_stock_name = i['shortName']
                            new_stock_change = i['regularMarketChangePercent']
                            shares_owned = form.cleaned_data['stocks_bought']
                            buying_price = form.cleaned_data['buying_price']

                            #Insert stock data into DB
                            stock_to_db = StockPortfolio(
                                            user=user,
                                            symbol=new_stock.upper(),
                                            name=new_stock_name,
                                            price=new_stock_price,
                                            change=new_stock_change,
                                            shares_owned=shares_owned,
                                            buying_price=buying_price,
                                            gain_loss= 0,
                                            signal= 0
                                            )
                            stock_to_db.save()

                            messages.success(request, new_stock.upper() + ' succesfully added to portfolio!')
                            add_success_message = "Stock successfully added to portfolio!"

                            #Determine gain or loss amount
                            stock = StockPortfolio.objects.get( user=user, symbol=new_stock.upper())
                            stocks = stock.shares_owned
                            bprice = stock.buying_price
                            price = stock.price
                            gain_loss = (stocks * price) - (stocks * bprice)
                            stock.gain_loss = gain_loss

                            #Determine signals based on prediction, current price and buying price
                            pred = Predictions.objects.get(symbol=new_stock.upper())
                            pred_day90 = pred.day90
                            if stock.buying_price < stock.price and stock.buying_price < pred_day90:
                                signal = 'SELL OR HOLD'
                            elif stock.buying_price > stock.price and stock.buying_price < pred_day90:
                                signal = 'HOLD'
                            elif stock.buying_price < stock.price and stock.buying_price > pred_day90:
                                signal = 'SELL'
                            elif stock.buying_price > stock.price and  stock.buying_price > pred_day90:
                                signal = 'HOLD'
                            stock.signal = signal
                            stock.save()


                            for stock in stock_list:        
                                choice1 = stock.symbol  

                            #Getting and plotting data from functions.py to render in portfolio.html
                            candlestick1 = candles1(choice1)

                            #Get current price and percent change from database for chart with user symbol choice 
                            chart_values1 = StockPortfolio.objects.filter(user=user, symbol=choice1)

                            pred_list = Predictions.objects.filter(symbol=choice1)

                            context = {
                                'stock_list': stock_list,
                                'today_date': today_date,
                                'add_success_message': add_success_message,
                                'choice1' : choice1,
                                'candlestick1' : candlestick1,
                                'chart_values1' : chart_values1,
                                'pred_list' : pred_list,
                                'theme_user' : theme_user
                            }
                            return render(request, 'portfolio.html', context)

                    except Exception:  # if symbol is not correct
                        pass
                        messages.error(request, 'Insert correct symbol!')
                        error_message = "Insert correct symbol!"

                        for stock in stock_list:        
                            choice1 = stock.symbol  

                        #Getting and plotting data from functions.py to render in portfolio.html
                        candlestick1 = candles1(choice1)

                        #Get current price and percent change from database for chart with user symbol choice 
                        chart_values1 = StockPortfolio.objects.filter(user=user, symbol=choice1)

                        pred_list = Predictions.objects.filter(symbol=choice1)

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'error_message': error_message,
                            'choice1' : choice1,
                            'candlestick1' : candlestick1,
                            'chart_values1' : chart_values1,
                            'pred_list' : pred_list,
                            'theme_user' : theme_user
                        }
                        return render(request, 'portfolio.html', context)

                else:  # if symbol is already in your portfolio
                    messages.error(request, 'Stock is already in your portfolio!')
                    stock_exists_message = "Stock is already in your portfolio!"

                    for stock in stock_list:        
                        choice1 = stock.symbol  

                    #Getting and plotting data from functions.py to render in portfolio.html
                    candlestick1 = candles1(choice1)

                    #Get current price and percent change from database for chart with user symbol choice 
                    chart_values1 = StockPortfolio.objects.filter(user=user, symbol=choice1)

                    pred_list = Predictions.objects.filter(symbol=choice1)

                    context = {
                        'stock_list': stock_list,
                        'today_date': today_date,
                        'stock_exists_message': stock_exists_message,
                        'choice1' : choice1,
                        'candlestick1' : candlestick1,
                        'chart_values1' : chart_values1,
                        'pred_list' : pred_list,
                        'theme_user' : theme_user
                    }
                    return render(request, 'portfolio.html', context)

            else:  # if form was incorrectly filled in
                messages.error(request, 'Invalid Form!')
                error_message = "Invalid Form!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'error_message': error_message,
                    'choice1' : choice1,
                    'candlestick1' : candlestick1,
                    'chart_values1' : chart_values1,
                    'pred_list' : pred_list,
                    'theme_user' : theme_user
                }
                return render(request, 'portfolio.html', context)

    elif 'remove_stock' in request.POST:  # if user was trying to remove stock from portfolio

        symbol = str(request.POST.get('stock_symbol'))

        if StockPortfolio.objects.filter(user=user,  symbol=symbol).count() > 0:  # if inserted stock is in portfolio

            logger.info('Removing ' + symbol + ' from stock portfolio')

            StockPortfolio.objects.filter( user=user, symbol=symbol).delete()
            stock_list = StockPortfolio.objects.filter(user_id=user)

            messages.success(request, symbol + ' succesfully deleted from portfolio!')
            delete_success_message = "Stock successfully removed from portfolio!"

            for stock in stock_list:
                choice1 = stock.symbol 

            #Getting and plotting data from functions.py to render in portfolio.html
            candlestick1 = candles1(choice1)

            #Get current price and percent change from database for chart with user symbol choice 
            chart_values1 = StockPortfolio.objects.filter(user=user, symbol=choice1)

            pred_list = Predictions.objects.filter(symbol=choice1)

            context = {
                'stock_list': stock_list,
                'today_date': today_date,
                'delete_success_message': delete_success_message,
                'choice1' : choice1,
                'candlestick1' : candlestick1,
                'chart_values1' : chart_values1,
                'pred_list' : pred_list,
                'theme_user' : theme_user
            }
            return render(request, 'portfolio.html', context)

    else:  # if there was no POST request - the whole portfolio should be updated

        stocks = StockPortfolio.objects.filter(user_id=user)  # This returns queryset

        for stock in stocks:

            url = "https://yfapi.net/v6/finance/quote"

            querystring = {"symbols":stock.symbol}

            headers = {
                'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"  
            }

            r = requests.request("GET", url, headers=headers, params=querystring)
            data = r.json()

            response = data['quoteResponse']
            result = response['result']

            for i in result:

                stock.price = decimal.Decimal(i['regularMarketPrice'])
                stock.change = i['regularMarketChangePercent']

            gain_loss = (stock.shares_owned * stock.price) - (stock.shares_owned * stock.buying_price)
            stock.gain_loss = gain_loss

            pred = Predictions.objects.get(symbol=stock.symbol)
            pred_day90 = pred.day90
            if stock.buying_price < stock.price and stock.buying_price < pred_day90:
                signal = 'SELL OR HOLD'
            elif stock.buying_price > stock.price and stock.buying_price < pred_day90:
                signal = 'HOLD'
            elif stock.buying_price < stock.price and stock.buying_price > pred_day90:
                signal = 'SELL'
            elif stock.buying_price > stock.price and  stock.buying_price > pred_day90:
                signal = 'HOLD'
            stock.signal = signal

            # update current lines
            stock.save(update_fields=['price', 'change', 'gain_loss', 'signal'])  # do not create new object in db,

            if request.method == 'POST':
                choice1 = request.POST.get('stock_selected1', '')
            else:
                choice1 = stock.symbol 

            candlestick1 = candles1(choice1)

            chart_values1 = StockPortfolio.objects.filter(user=user, symbol=choice1)

            pred_list = Predictions.objects.filter(symbol=choice1)
            
        context = {
            'stock_list': stock_list,
            'today_date': today_date,
            'choice1' : choice1,
            'candlestick1' : candlestick1,
            'chart_values1' : chart_values1,
            'pred_list' : pred_list,
            'theme_user' : theme_user
        }

        logger.info('Refreshing stock list')

        return render(request, 'portfolio.html', context)


@csrf_exempt    
@login_required
def watchlistView(request):

    user_id = request.user.id

    user = PortfolioUser.objects.filter(user=user_id)[0]
    watch_list = Watchlist.objects.filter(user_id=user)

    today_date = time.strftime("%m.%d.%Y")

    #Get stock the user selected from dropdown for loading to chart
    if request.method == 'POST':
        choice1 = request.POST.get('stock_selected1', '')
    else:
        choice1 = '' 

    #Getting and plotting data from functions.py to render in portfolio.html
    candlestick3 = candles3(choice1)

    #Get current price and percent change from database for chart with user symbol choice 
    chart_values3 = Watchlist.objects.filter(user=user, symbol=choice1)

    #Get predictions from DB
    pred_list = Predictions.objects.filter(symbol=choice1)

    #Get users theme
    theme_user = Theme.objects.filter(user=user)
    
    if 'add_stock' in request.POST:

            form = AddWatchlistForm(request.POST)

            if form.is_valid():  # form validation
                new_stock = request.POST.get("add_stock", "")

                if not Watchlist.objects.filter(user=user, symbol=new_stock.upper()):  # stock not already in watchlist

                    logger.info('Adding ' + new_stock.upper() + ' to watchlist')

                    try:  # try to add stock to watchlist
                        url = "https://yfapi.net/v6/finance/quote"

                        querystring = {"symbols":new_stock.upper()}

                        headers = {
                        'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"  
                        }

                        r = requests.request("GET", url, headers=headers, params=querystring)
                        data = r.json()

                        response = data['quoteResponse']
                        result = response['result']

                        for i in result:

                            new_stock_price = i['regularMarketPrice']
                            new_stock_name = i['shortName']
                            new_stock_change = i['regularMarketChangePercent']

                            #Insert stock to DB
                            stock_to_db = Watchlist(
                                            user=user,
                                            symbol=new_stock.upper(),
                                            name=new_stock_name,
                                            price=new_stock_price,
                                            change=new_stock_change,
                                            )
                            stock_to_db.save()

                            messages.success(request, new_stock.upper() + ' succesfully added to watchlist!')
                            add_success_message = "Stock successfully added to watchlist!"

                            #Determine suggestion based on prediction and current price
                            stock = Watchlist.objects.get( user=user, symbol=new_stock.upper())
                            pred = Predictions.objects.get(symbol=stock.symbol)
                            pred_day90 = pred.day90
                            if pred_day90 > stock.price + 5:
                                signal = 'BUY'
                            elif pred_day90 <= stock.price:
                                signal = 'WAIT'
                            stock.signal = signal
                            stock.save()

                            for stock in watch_list:
                                choice1 = stock.symbol 

                            #Getting and plotting data from functions.py to render in portfolio.html
                            candlestick3 = candles3(choice1)

                            #Get current price and percent change from database for chart with user symbol choice 
                            chart_values3 = Watchlist.objects.filter(user=user, symbol=choice1)

                            pred_list = Predictions.objects.filter(symbol=choice1)

                            context = {
                                'watch_list': watch_list,
                                'today_date': today_date,
                                'add_success_message': add_success_message,
                                'choice1' : choice1,
                                'candlestick3' : candlestick3,
                                'chart_values3' : chart_values3,
                                'pred_list' : pred_list,
                                'theme_user' : theme_user
                            }
                            return render(request, 'watchlist.html', context)

                    except Exception:  # if symbol is not correct
                        pass
                        messages.error(request, 'Insert correct symbol!')
                        error_message = "Insert correct symbol!"

                        context = {
                            'watch_list': watch_list,
                            'today_date': today_date,
                            'error_message': error_message,
                            'choice1' : choice1,
                            'candlestick3' : candlestick3,
                            'chart_values3' : chart_values3,
                            'pred_list' : pred_list,
                            'theme_user' : theme_user
                        }
                        return render(request, 'watchlist.html', context)

                else:  # if symbol is already in your watchlist
                    messages.error(request, 'Stock is already in your watchlist!')
                    stock_exists_message = "Stock is already in your watchlist!"

                    for stock in watch_list:        
                        choice1 = stock.symbol  

                    #Getting and plotting data from functions.py to render in portfolio.html
                    candlestick3 = candles3(choice1)

                    #Get current price and percent change from database for chart with user symbol choice 
                    chart_values3 = Watchlist.objects.filter(user=user, symbol=choice1)

                    pred_list = Predictions.objects.filter(symbol=choice1)

                    context = {
                        'watch_list': watch_list,
                        'today_date': today_date,
                        'stock_exists_message': stock_exists_message,
                        'choice1' : choice1,
                        'candlestick3' : candlestick3,
                        'chart_values3' : chart_values3,
                        'pred_list' : pred_list,
                        'theme_user' : theme_user
                    }
                    return render(request, 'watchlist.html', context)

            else:  # if form was incorrectly filled in
                messages.error(request, 'Invalid Form!')
                error_message = "Invalid form!"

                context = {
                    'watch_list': watch_list,
                    'today_date': today_date,
                    'error_message': error_message,
                    'choice1' : choice1,
                    'candlestick3' : candlestick3,
                    'chart_values3' : chart_values3,
                    'pred_list' : pred_list,
                    'theme_user' : theme_user
                }
                return render(request, 'watchlist.html', context)

    elif 'remove_stock' in request.POST:  # if user was trying to remove stock from watchlist

        symbol = str(request.POST.get('stock_symbol'))

        if Watchlist.objects.filter(user=user,  symbol=symbol).count() > 0:  # if inserted stock is in watchlist

            logger.info('Removing ' + symbol + ' from watchlist')

            Watchlist.objects.filter( user=user, symbol=symbol).delete()
            watch_list = Watchlist.objects.filter(user_id=user)

            messages.success(request, symbol + ' succesfully deleted from watchlist!')
            delete_success_message = "Stock successfully removed from watchlist!"

            for stock in watch_list:
                choice1 = stock.symbol 

            #Getting and plotting data from functions.py to render in portfolio.html
            candlestick3 = candles3(choice1)

            #Get current price and percent change from database for chart with user symbol choice 
            chart_values3 = Watchlist.objects.filter(symbol=choice1)

            pred_list = Predictions.objects.filter(symbol=choice1)

            context = {
                'watch_list': watch_list,
                'today_date': today_date,
                'delete_success_message': delete_success_message,
                'choice1' : choice1,
                'candlestick3' : candlestick3,
                'chart_values3' : chart_values3,
                'pred_list' : pred_list,
                'theme_user' : theme_user
            }
            return render(request, 'watchlist.html', context)

    else:  # if there was no POST request - the whole watchlist should be updated

        stocks = Watchlist.objects.filter(user_id=user)  # This returns queryset

        for stock in stocks:

            url = "https://yfapi.net/v6/finance/quote"

            querystring = {"symbols":stock.symbol}

            headers = {
                'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"  
            }

            r = requests.request("GET", url, headers=headers, params=querystring)
            data = r.json()

            response = data['quoteResponse']
            result = response['result']

            for i in result:

                stock.price = decimal.Decimal(i['regularMarketPrice'])
                stock.change = i['regularMarketChangePercent']

                pred = Predictions.objects.get(symbol=stock.symbol)
                pred_day90 = pred.day90
                if pred_day90 > stock.price + 5:
                    signal = 'BUY'
                elif pred_day90 <= stock.price:
                    signal = 'WAIT'
                stock.signal = signal


                stock.save(update_fields=['price', 'change', 'signal'])  # do not create new object in db,
                # update current lines

                if request.method == 'POST':
                    choice1 = request.POST.get('stock_selected1', '')
                else:
                    choice1 = stock.symbol 

                candlestick3 = candles1(choice1)

                chart_values3 = Watchlist.objects.filter(user=user, symbol=choice1)

                pred_list = Predictions.objects.filter(symbol=choice1)

        context = {
            'watch_list': watch_list,
            'today_date': today_date,
            'choice1' : choice1,
            'candlestick3' : candlestick3,
            'chart_values3' : chart_values3,
            'pred_list' : pred_list,
            'theme_user' : theme_user
        }

        logger.info('Refreshing watchlist')

        return render(request, 'watchlist.html', context)
        

@login_required
def notificationsView(request):

    user_id = request.user.id
    user = PortfolioUser.objects.filter(user=user_id)[0]

    today_date = time.strftime("%m.%d.%Y")

    stock_list = StockPortfolio.objects.filter(user_id=user)

    stocks = StockPortfolio.objects.filter(user_id=user)  #This returns queryset

    #Get users theme
    theme_user = Theme.objects.filter(user=user)

    #If stockexists within user portfolio, update and render to app
    if stocks.exists():

        for stock in stocks:

            url = "https://yfapi.net/v6/finance/quote"

            querystring = {"symbols":stock.symbol}

            headers = {
                'x-api-key': "iFc6RqsSZ31mlsJY7frhf3RkQbjyn4325Dztkxy2"  
            }

            r = requests.request("GET", url, headers=headers, params=querystring)
            data = r.json()

            response = data['quoteResponse']
            result = response['result']

            for i in result:

                stock.price = decimal.Decimal(i['regularMarketPrice'])
                stock.change = i['regularMarketChangePercent']

            gain_loss = (stock.shares_owned * stock.price) - (stock.shares_owned * stock.buying_price)
            stock.gain_loss = gain_loss

            pred = Predictions.objects.get(symbol=stock.symbol)
            pred_day90 = pred.day90
            if stock.buying_price < stock.price and stock.buying_price < pred_day90:
                signal = 'SELL OR HOLD'
            elif stock.buying_price > stock.price and stock.buying_price < pred_day90:
                signal = 'HOLD'
            elif stock.buying_price < stock.price and stock.buying_price > pred_day90:
                signal = 'SELL'
            elif stock.buying_price > stock.price and  stock.buying_price > pred_day90:
                signal = 'HOLD'
            stock.signal = signal

            # update current lines
            stock.save(update_fields=['price', 'change', 'gain_loss', 'signal'])


            context={
                'stock_list' : stock_list,
                'today_date' : today_date,
                'theme_user' : theme_user
            }

            return render(request, 'notifications.html', context)
    else:
        context={
          'theme_user' : theme_user,
          'today_date' : today_date, 
        }
        return render(request, 'notifications.html', context)

@csrf_exempt
@login_required
def settingsView(request):
    user_id = request.user.id
    users = User.objects.filter(id=user_id)[0]
    user = PortfolioUser.objects.filter(user=user_id)[0]

    #Get users theme
    theme_user = Theme.objects.filter(user=user)
    
    context={
        'theme_user' : theme_user
    }
    #Change users password
    u = User.objects.get(username=users.username)
    if request.method == "POST":
        change_password = request.POST.get('change_password', '')
        u.set_password(change_password)
        u.save()

        messages.success(request, 'Your password has been changed. Please log back in.')
        return redirect('Landing:login')


        
    else:
        return render(request, 'settings.html', context)

@csrf_exempt
def theme(request):
    user_id = request.user.id
    user = PortfolioUser.objects.filter(user=user_id)[0]

    color = request.GET.get('color')
    #If user choice is dark.
    if color == 'dark':
        #If a theme exists, update field with new choice.
        if Theme.objects.filter(user_id=user).exists():
            user_theme1 = Theme.objects.get(user_id=user)
            user_theme1.user_id = user
            user_theme1.color = 'dark'
            user_theme1.save()
        #If user doesn't have a theme, assign new theme.
        else:
            user1 = Theme(user=user, color='dark')
            user1.save()
        messages.success(request, 'Your theme has been changed to dark mode.')

    #If user choice is light
    elif color == 'light':
        #If a theme exists, update field with new choice.
        if Theme.objects.filter(user_id=user).exists():
            user_theme2 = Theme.objects.get(user_id=user)
            user_theme2.user_id = user
            user_theme2.color = 'light'
            user_theme2.save()
        #If user doesn't have a theme, assign new theme.
        else:
            user2 = Theme(user_id=user, color='light')
            user2.save()
        messages.success(request, 'Your theme has been changed to light mode.')

    return redirect('Portfolios:settings')

@csrf_exempt
def email_alert(request):
    user_id = request.user.id
    user = PortfolioUser.objects.filter(user=user_id)[0]

    choice = request.GET.get('choice')
    #If user choice is notifications On.
    if choice == 'On':
        #If user has a choice, update with new one.
        if Notifications.objects.filter(user_id=user).exists():
            user_choice1 = Notifications.objects.get(user_id=user)
            user_choice1.user_id = user
            user_choice1.status = 'On'
            user_choice1.save()
        #If user dosn't have a choice, set new.
        else:
            user_alert1 = Notifications(user=user, status='On')
            user_alert1.save()
        messages.success(request, 'Your email notifications are On.')

    #If user choice is notifications Off.
    elif choice == 'Off':
        #If user has a choice, update with new one.
        if Notifications.objects.filter(user_id=user).exists():
            user_choice2 = Notifications.objects.get(user_id=user)
            user_choice2.user_id = user
            user_choice2.status = 'Off'
            user_choice2.save()
        #If user dosn't have a choice, set new.
        else:
            user_alert2 = Notifications(user=user, status='Off')
            user_alert2.save()
        messages.success(request, 'Your email notifications are Off.')

    return redirect('Portfolios:settings')

#Function to send email when user creates a ticket.
@csrf_exempt
@login_required
def helpView(request):
    user_id = request.user.id
    user = PortfolioUser.objects.filter(user=user_id)[0]

    #Get users theme
    theme_user = Theme.objects.filter(user=user)

    context={
        'theme_user' : theme_user
    }

    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        user_email = request.POST.get('user_email', '')
        ticket_reason = request.POST.get('ticket_reason', '')
        staff_email = 'sightapptickets@outlook.com'
        
        
        subject = "New Ticket has been created"
        email_template_name = "ticket_email.txt"
        c = {
        "name":name,
        "phone":phone,
        "email":user_email,
        "ticket_reason":ticket_reason,
        }
        email = render_to_string(email_template_name, c)
        try:
            send_mail(subject, email, 'sightstockapp@outlook.com' , [staff_email], fail_silently=False)
        except BadHeaderError:

            return HttpResponse('Invalid header found.')
            
        messages.success(request, 'Ticket has been created. One of our staff will be in contact with you shortly.')
        return redirect ("help")
			
	

    return render(request, 'help.html', context)       





    