from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser




def indexView(request):

    return render(request, 'dashboardindex.html')  