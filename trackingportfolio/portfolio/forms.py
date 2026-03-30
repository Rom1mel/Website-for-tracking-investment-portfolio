from .models import PortfolioAsset
from django.forms import ModelForm

class PortfolioAssetForm(ModelForm):
    class Meta:
        model = PortfolioAsset
        fields = ['asset', 'count', 'price']