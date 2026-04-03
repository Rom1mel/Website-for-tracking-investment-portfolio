from django.shortcuts import render, redirect
from .models import PortfolioAsset, Portfolio
from .forms import PortfolioForm
from django.db.models import Sum, F, FloatField, ExpressionWrapper

def portfolio(request):
    portfolio_id = request.GET.get('portfolio_id', 'all')
    if portfolio_id == 'all':
        assets = (PortfolioAsset.objects.
            filter(portfolio__user=request.user).values('asset__name').
            annotate(total_count = Sum('count'), total_value =Sum(F('count')*F('price'))).
            annotate(avg_price=ExpressionWrapper(
                F('total_value') / F('total_count'),
                output_field=FloatField())))
    else:
        assets = (PortfolioAsset.objects.
            filter(portfolio_id=portfolio_id, portfolio__user=request.user).values('asset__name').
            annotate(total_count = Sum('count'), total_value =Sum('price')).
            annotate(avg_price=ExpressionWrapper(F('total_value') / F('total_count'),
                 output_field=FloatField())))
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