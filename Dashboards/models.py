from django.db import models
from Portfolios.models import PortfolioUser



class Predictions(models.Model):
  '''Predictions Table to maintain stocks predictions'''
  symbol = models.CharField(default='', max_length=1)
  day1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day14 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day30 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day90 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Theme(models.Model):
  '''Theme table to maintain the users theme of choice'''
  user = models.ForeignKey(PortfolioUser, on_delete=models.CASCADE)
  color = models.CharField(max_length=1000)