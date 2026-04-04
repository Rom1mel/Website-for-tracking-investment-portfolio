from deals.models import Deal
from django.forms import ModelForm
from .models import Portfolio, Asset


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['type', 'portfolio', 'asset', 'value', 'price_per_unit']

    def __init__(self, *args, user=None, show_all=False, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["portfolio"].queryset = Portfolio.objects.filter(user=user)

        if show_all:
            self.fields["asset"].queryset = Asset.objects.all()
        else:
            self.fields["asset"].queryset = Asset.objects.filter(type='top_crypto')

class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'type']