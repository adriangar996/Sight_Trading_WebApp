# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from Portfolios.models import StockPortfolio, PortfolioUser


# def user_info(user_id):

#     user = PortfolioUser.objects.filter(user=user_id)
#     f_name = {'first_name' : user.first_name}
#     l_name = {'last_name' : user.last_name}
#     email = {'user' : user.user}

#     return {'f_name' : f_name, 'l_name' : l_name, 'email' : email}