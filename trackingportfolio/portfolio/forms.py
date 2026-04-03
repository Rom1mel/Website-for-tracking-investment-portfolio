from deals.models import Deal
from django.forms import ModelForm
from .models import Portfolio

class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['type', 'portfolio', 'asset', 'value', 'price_per_unit']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["portfolio"].queryset = Portfolio.objects.filter(user=user)
class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'type']