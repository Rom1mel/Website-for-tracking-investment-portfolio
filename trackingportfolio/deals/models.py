from django.db import models
from portfolio.models import Asset, Portfolio

class Deal(models.Model):
    type = models.CharField(max_length=50)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transaction')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transaction')
    value = models.PositiveIntegerField()
    price_per_unit = models.PositiveIntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.type