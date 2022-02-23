from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser



@login_required
def portfolioView(request):

    return render(request, 'portfolio.html')

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

# from django.shortcuts import render
# from yahoo_finance import Share
# import time
# import decimal
# import logging
# from Portfolios.models import StockPortfolio, PortfolioUser
# from .forms import AddStockForm
# from django.contrib.auth.decorators import login_required


# # CREATING LOGGER
# logger = logging.getLogger('LOG')
# logger.setLevel(logging.INFO)

# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)

# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # add formatter to ch
# ch.setFormatter(formatter)

# # add ch to logger
# logger.addHandler(ch)

# @login_required
# def portfolio(request):
#     """
#     function, that allows to add or remove stocks and displays them in portfolio
    
#     :param request: POST request that defines weather to add or remove stock options to portfolio
#     :return: portfolio.html with context dictionary that has all the stock options that you have added to portfolio
#     """

#     stock_list = StockPortfolio.objects.order_by('price')[:10]

#     today_date = time.strftime("%d.%m.%Y %H:%M")

#     #user_id = request.user.id
#     if 'add_stock' in request.POST:

#             form = AddStockForm(request.POST)

#             if form.is_valid():  # form validation
#                 new_stock = request.POST.get("add_stock", "")

#                 if not StockPortfolio.objects.filter(symbol=new_stock.upper()):  # stock not already in portfolio

#                     logger.info('Adding ' + new_stock.upper() + ' to stock portfolio')

#                     try:  # try to add stock to portfolio
#                         stock_object = Share(new_stock)
#                         new_stock_name = stock_object.get_name()
#                         new_stock_price = stock_object.get_price()
#                         new_stock_change = stock_object.get_change()
#                         shares_owned = form.cleaned_data['stocks_bought']
#                         buying_price = form.cleaned_data['buying_price']

#                         stock_to_db = StockPortfolio(symbol=new_stock.upper(),
#                                              name=new_stock_name,
#                                              price=new_stock_price,
#                                              change=new_stock_change,
#                                              shares_owned=shares_owned,
#                                              buying_price=buying_price,
#                                              balance=0
#                                              )
#                         stock_to_db.save()

#                         add_success_message = "Stock successfully added to portfolio!"

#                         stock = StockPortfolio.objects.get(symbol=new_stock)
#                         stocks = stock.shares_owned
#                         bprice = stock.buying_price
#                         price = stock.price
#                         balance = (stocks * price) - (stocks * bprice)
#                         stock.balance = balance
#                         stock.save()

#                         context = {
#                             'stock_list': stock_list,
#                             'today_date': today_date,
#                             'add_success_message': add_success_message,
#                         }
#                         return render(request, 'Portfolio/portfolio.html', context)

#                     except Exception:  # if symbol is not correct
#                         pass
#                         error_message = "Insert correct symbol!"

#                         context = {
#                             'stock_list': stock_list,
#                             'today_date': today_date,
#                             'error_message': error_message,
#                         }
#                         return render(request, 'Portfolio/portfolio.html', context)

#                 else:  # if symbol is already in your portfolio
#                     stock_exists_message = "Stock is already in your portfolio!"

#                     context = {
#                         'stock_list': stock_list,
#                         'today_date': today_date,
#                         'stock_exists_message': stock_exists_message,
#                     }
#                     return render(request, 'Portfolio/portfolio.html', context)

#             else:  # if form was incorrectly filled in
#                 error_message = "Invalid form!"

#                 context = {
#                     'stock_list': stock_list,
#                     'today_date': today_date,
#                     'error_message': error_message,
#                 }
#                 return render(request, 'Portfolio/portfolio.html', context)

#     elif 'remove_stock' in request.POST:  # if user was trying to remove stock from portfolio

#         symbol = str(request.POST.get('stock_symbol'))

#         if StockPortfolio.objects.filter(symbol=symbol).count() > 0:  # if inserted stock is in portfolio

#             logger.info('Removing ' + symbol + ' from stock portfolio')

#             StockPortfolio.objects.filter(symbol=symbol).delete()
#             stock_list = StockPortfolio.objects.order_by('price')[:10]

#             delete_success_message = "Stock successfully removed from portfolio!"

#             context = {
#                 'stock_list': stock_list,
#                 'today_date': today_date,
#                 'delete_success_message': delete_success_message,
#             }
#             return render(request, 'Portfolio/portfolio.html', context)

#     else:  # if there was no POST request - the whole portfolio should be updated

#         stocks = StockPortfolio.objects.all()  # This returns queryset

#         for stock in stocks:
#             stock_object = Share(stock.symbol)

#             stock.price = decimal.Decimal(stock_object.get_price())
#             stock.change = stock_object.get_change()

#             balance = (stock.stocks_owned * stock.price) - (stock.stocks_owned * stock.buying_price)
#             stock.balance = balance

#             stock.save(update_fields=['price', 'change', 'balance'])  # do not create new object in db,
#             # update current lines

#         context = {
#             'stock_list': stock_list,
#             'today_date': today_date
#         }

#         logger.info('Refreshing stock list')

#         return render(request, 'Portfolio/portfolio.html', context)




