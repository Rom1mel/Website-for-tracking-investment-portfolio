from django.contrib.auth.models import User
from django.db import models

class Portfolio(models.Model):
    MIXED = 'mixed'
    CRYPTO = 'crypto'
    STOCK_MARKET = 'stock_market'
    STOCK_MARKET_RUS = 'stock_market_rus'
    STOCK_MARKET_US = 'stock_market_us'
    RAW_MATERIAL = 'raw_material'
    TYPE_CHOICES = (
        (MIXED, 'mixed'),
        (CRYPTO, 'crypto'),
        (STOCK_MARKET, 'stock_market'),
        (STOCK_MARKET_RUS, 'stock_market_rus'),
        (STOCK_MARKET_US, 'stock_market_us'),
        (RAW_MATERIAL, 'raw_material'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=MIXED)
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