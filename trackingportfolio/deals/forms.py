from django.forms import ModelForm
from django import forms
from .models import *
from portfolio.models import Portfolio, PortfolioAsset, Asset
from django.core.exceptions import ValidationError

class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['type', 'portfolio', 'asset', 'value', 'price_per_unit']

    asset = forms.ModelChoiceField(
        queryset=Asset.objects.none(),
        required=True,
    )
    def __init__(self, *args, user=None, show_all=False, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["portfolio"].queryset = Portfolio.objects.filter(user=user)

        if self.data.get("asset"):
            self.fields["asset"].queryset = Asset.objects.filter(
                id=self.data.get("asset")
            )

        if self.instance and self.instance.pk:
            self.fields["asset"].queryset = Asset.objects.filter(pk=self.instance.asset_id)
            self.fields['portfolio'].disabled = True

    def clean_portfolio(self):
        if self.instance and self.instance.pk:
            return self.instance.portfolio
        return self.cleaned_data.get('portfolio')

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

class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = ['type', 'portfolio', 'value']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["portfolio"].queryset = Portfolio.objects.filter(user=user)
