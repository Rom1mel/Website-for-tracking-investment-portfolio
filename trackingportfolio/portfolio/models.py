from django.contrib.auth.models import User
from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio')
    time_stamp = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name

class Asset(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default='')
    def __str__(self):
        return self.name

class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='portfolio')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='asset')
    count = models.PositiveIntegerField()
    price = models.FloatField()
    class Meta:
        unique_together = ['portfolio', 'asset']
    def __str__(self):
        return str(self.portfolio)