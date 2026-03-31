from django.shortcuts import render
from .models import PortfolioAsset

def portfolio(request):
    assets = PortfolioAsset.objects.filter(portfolio__user=request.user)
    return render(request, 'portfolio/portfolio.html', {'assets': assets})
