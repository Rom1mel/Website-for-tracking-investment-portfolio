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
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='asset')
    count = models.PositiveIntegerField()
    purchase_price_per_unit = models.PositiveIntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    type = models.CharField(max_length=50)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transaction')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transaction')
    value = models.PositiveIntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.type