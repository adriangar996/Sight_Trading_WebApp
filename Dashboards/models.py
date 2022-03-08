from django.db import models


class Predictions(models.Model):
  '''Predictions Table to maintain stocks predictions'''
  symbol = models.CharField(default='', max_length=1)
  day1 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day5 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day14 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day30 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  day90 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)