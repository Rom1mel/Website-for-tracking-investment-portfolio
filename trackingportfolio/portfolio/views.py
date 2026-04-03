from django.shortcuts import render, redirect
from .models import PortfolioAsset, Portfolio
from .forms import PortfolioForm

def portfolio(request):
    assets = PortfolioAsset.objects.filter(portfolio__user=request.user)
    return render(request, 'portfolio/portfolio.html', {'assets': assets})

def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            new_portfolio_data = form.save(commit=False)
            name = new_portfolio_data.name
            type = new_portfolio_data.type
            user = request.user
            Portfolio.objects.create(user=user, name=name, type=type)
        return redirect('portfolio')
    else:
        form = PortfolioForm()
        return render(request, 'portfolio/create_portfolio.html', {'form': form})