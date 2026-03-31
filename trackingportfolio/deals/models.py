from django.db import models
from portfolio.models import Asset, Portfolio

class Deal(models.Model):
    BUY = 'buy'
    SELL = 'sell'

    TYPE_CHOICES = [
        (BUY, 'Покупка'),
        (SELL, 'Продажа'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=BUY)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transaction')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transaction')
    value = models.PositiveIntegerField()
    price_per_unit = models.PositiveIntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.type