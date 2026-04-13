from django.forms import ModelForm, forms
from .models import *
from portfolio.models import Portfolio, PortfolioAsset, Asset
from django.core.exceptions import ValidationError



class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['type', 'portfolio', 'asset', 'value']
    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["portfolio"].queryset = Portfolio.objects.filter(user=user)
            self.fields["asset"].queryset = Asset.objects.filter(asset__portfolio__user=user).distinct()
    def clean(self):
        cleaned_data = super().clean()
        portfolio = cleaned_data.get("portfolio")
        asset = cleaned_data.get("asset")
        if portfolio and asset:
            asset_in_portfolio = PortfolioAsset.objects.filter(asset=asset, portfolio=portfolio).exists()
            if not asset_in_portfolio:
                raise ValidationError("Актив не принадлежит выбранному портфелю")
        return cleaned_data