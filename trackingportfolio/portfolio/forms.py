from deals.models import Deal
from django.forms import ModelForm
from .models import Portfolio, Asset

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'type']