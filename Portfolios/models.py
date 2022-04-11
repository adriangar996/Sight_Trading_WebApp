'''models.py for relationship between portfolio and user'''
from django.db import models
from django.contrib.auth.models import User


class PortfolioUser(models.Model):
  '''Add Portfolio data to User'''
  first_name = models.CharField(default='', max_length=1)
  last_name = models.CharField(default='', max_length=1)
  user = models.OneToOneField(User, on_delete=models.CASCADE)

class StockPortfolio(models.Model):
  '''Stock Table to maintain the stock owned'''
  user = models.ForeignKey(PortfolioUser, on_delete=models.CASCADE)
  symbol = models.CharField(default='', max_length=1)
  name = models.CharField(default='', max_length=200)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  shares_owned = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  gain_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  signal = models.CharField(default='', max_length=1)

class Watchlist(models.Model):
  '''Watchlist Table to maintain stocks on watchlist'''
  user = models.ForeignKey(PortfolioUser, on_delete=models.CASCADE)
  symbol = models.CharField(default='', max_length=1)
  name = models.CharField(default='', max_length=200)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  signal = models.CharField(default='', max_length=1)

  class Meta:
    '''The ForeignKey i.e. user and a stock symbol must be unique'''
    unique_together = ('user', 'symbol')



