from django.shortcuts import render, redirect
from .models import PortfolioAsset, Portfolio
from .forms import PortfolioForm

def portfolio(request):
    portfolio_id = request.GET.get('portfolio_id', 'all')
    if portfolio_id == 'all':
        assets = PortfolioAsset.objects.filter(portfolio__user=request.user)
    else:
        assets = PortfolioAsset.objects.filter(portfolio_id=portfolio_id, portfolio__user=request.user)
    portfolios = Portfolio.objects.filter(user=request.user)
    data = {'assets': assets,
        'portfolios': portfolios,
        'selected': portfolio_id}
    return render(request, 'portfolio/portfolio.html', data)

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