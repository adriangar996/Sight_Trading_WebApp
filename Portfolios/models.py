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
  
  @staticmethod
  def owned(user_id, stock_symbol, num_shares, cost_per_share):
    '''Create stock row with number of shares owned and price per share owned or add num of shares owned'''
    stock_user = PortfolioUser.objects.get(user=user_id)
    stock_user.buying_price += float(cost_per_share) * int(num_shares)
    stock_user.save()
    result = StockPortfolio.objects.get_or_create(symbol=stock_symbol, user=stock_user)[0]
    result.shares_owned += int(num_shares)
    result.save()

  @staticmethod
  def change_owned(user_id, stock_symbol, num_shares, cost_per_share):
    '''Create stock row with decreased number of shares or delete shares owned'''
    stock_user = PortfolioUser.objects.get(user=user_id)
    result = StockPortfolio.objects.filter(stock=stock_symbol, user=stock_user)[0]
    result.shares_owned -= int(num_shares)
    if result.shares_owned < 0:
      result.shares_owned = 0
      stock_user.buying_price += float(cost_per_share) * result.shares_owned
    else:
      stock_user.buying_price += float(cost_per_share) * int(num_shares)
    stock_user.save()
    if result.shares_owned == 0:
      result.delete()
    else:
      result.save()