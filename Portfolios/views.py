from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Portfolios.models import StockPortfolio, PortfolioUser
from yahoo_finance import Share
import time
import decimal
from .forms import AddStockForm
from .functions import *
import logging
import requests


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


@login_required
def portfolioView(request):

    user_id = request.user.id

    user = PortfolioUser.objects.filter(user=user_id)[0]
    stock_list = StockPortfolio.objects.all()

    today_date = time.strftime("%d.%m.%Y %H:%M")

    
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

                        for i in result:

                            new_stock_price = i['regularMarketPrice']
                            new_stock_name = i['shortName']
                            new_stock_change = i['regularMarketChangePercent']
                            shares_owned = form.cleaned_data['stocks_bought']
                            buying_price = form.cleaned_data['buying_price']


                            stock_to_db = StockPortfolio(
                                            user=user,
                                            symbol=new_stock.upper(),
                                            name=new_stock_name,
                                            price=new_stock_price,
                                            change=new_stock_change,
                                            shares_owned=shares_owned,
                                            buying_price=buying_price,
                                            gain_loss= 0
                                            )
                            stock_to_db.save()

                            add_success_message = "Stock successfully added to portfolio!"

                            stock = StockPortfolio.objects.get( user=user, symbol=new_stock.upper())
                            stocks = stock.shares_owned
                            bprice = stock.buying_price
                            price = stock.price
                            gain_loss = (stocks * price) - (stocks * bprice)
                            stock.gain_loss = gain_loss
                            stock.save()


                            context = {
                                'stock_list': stock_list,
                                'today_date': today_date,
                                'add_success_message': add_success_message,
                            }
                            return render(request, 'portfolio.html', context)

                    except Exception:  # if symbol is not correct
                        pass
                        error_message = "Insert correct symbol!"

                        context = {
                            'stock_list': stock_list,
                            'today_date': today_date,
                            'error_message': error_message,
                        }
                        return render(request, 'portfolio.html', context)

                else:  # if symbol is already in your portfolio
                    stock_exists_message = "Stock is already in your portfolio!"

                    context = {
                        'stock_list': stock_list,
                        'today_date': today_date,
                        'stock_exists_message': stock_exists_message,
                    }
                    return render(request, 'portfolio.html', context)

            else:  # if form was incorrectly filled in
                error_message = "Invalid form!"

                context = {
                    'stock_list': stock_list,
                    'today_date': today_date,
                    'error_message': error_message,
                }
                return render(request, 'portfolio.html', context)

    elif 'remove_stock' in request.POST:  # if user was trying to remove stock from portfolio

        symbol = str(request.POST.get('stock_symbol'))

        if StockPortfolio.objects.filter(user=user,  symbol=symbol).count() > 0:  # if inserted stock is in portfolio

            logger.info('Removing ' + symbol + ' from stock portfolio')

            StockPortfolio.objects.filter( user=user, symbol=symbol).delete()
            stock_list = StockPortfolio.objects.order_by('price')[:10]

            delete_success_message = "Stock successfully removed from portfolio!"

            context = {
                'stock_list': stock_list,
                'today_date': today_date,
                'delete_success_message': delete_success_message,
            }
            return render(request, 'portfolio.html', context)

    else:  # if there was no POST request - the whole portfolio should be updated

        stocks = StockPortfolio.objects.all()  # This returns queryset

        for stock in stocks:
            #stock_object = Share(stock.symbol)

            #stock.price = decimal.Decimal(stock_object.get_price())
            #stock.change = stock_object.get_percent_change()

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

            stock.save(update_fields=['price', 'change', 'gain_loss'])  # do not create new object in db,
            # update current lines

        context = {
            'stock_list': stock_list,
            'today_date': today_date
        }

        logger.info('Refreshing stock list')

        return render(request, 'portfolio.html', context)






    

def watchlistView(request):

    return render(request, 'watchlist.html')

def notificationsView(request):

    return render(request, 'notifications.html')

def accountView(request):

    return render(request, 'account.html')

def settingsView(request):

    return render(request, 'settings.html')

def helpView(request):

    return render(request, 'help.html')       





   