from django.shortcuts import render, redirect
from .models import PortfolioAsset, Portfolio, Price, Asset
from .forms import PortfolioForm
from django.db.models import Sum, F, FloatField, ExpressionWrapper, OuterRef, Subquery
from deals.models import Deal, Payment
from portfolio.services.profit_service import culculate_profit, culculate_asset_profit


def portfolio(request):
    portfolio_id = request.GET.get('portfolio_id', 'all')
    if portfolio_id == 'all': #Если выбраны все портфели
        latest_price = Price.objects.filter(asset=OuterRef('asset')).values('price')[:1] #Подзапрос для получения цены
        assets = (PortfolioAsset.objects.
            filter(portfolio__user=request.user).values('asset__name', 'asset_id', 'portfolio_id').
            annotate(total_count = Sum('count'), total_value =Sum(F('count')*F('price'))).
            annotate(avg_price=ExpressionWrapper(
                F('total_value') / F('total_count'),
                output_field=FloatField())).
            annotate(total_price = Subquery(latest_price) * F('total_count'),
                     profit=F('total_price') - F('total_value')))
        total_profit = assets.aggregate(total_profit=Sum('profit'))['total_profit'] or 0
        assets = list(assets)
        for asset in assets: #Добавление поля с полный прибылью каждого актива после запроса к бд
            asset['profit_asset'] = culculate_asset_profit(asset['portfolio_id'], asset['asset_id'])
        selected_portfolios = Portfolio.objects.filter(user=request.user)
        balance = selected_portfolios.aggregate(total_balance=Sum('balance'))['total_balance'] or 0
        portfolios = Portfolio.objects.filter(user=request.user)
        profit = 0
        for portfolio_user in portfolios:
            profit += culculate_profit(portfolio_user.id)

    else: #Если выбран конкретный портфель
        latest_price = Price.objects.filter(asset=OuterRef('asset')).values('price')[:1]  # Подзапрос для получения цены
        assets = (PortfolioAsset.objects.
            filter(portfolio_id=portfolio_id, portfolio__user=request.user).values('asset__name', 'asset_id', 'portfolio_id').
            annotate(total_count = Sum('count'), total_value =Sum(F('count') * F('price'))).
            annotate(avg_price=ExpressionWrapper(F('total_value') / F('total_count'),
                 output_field=FloatField())).
            annotate(total_price = Subquery(latest_price) * F('total_count'),
                     profit=F('total_price') - F('total_value'),))

        total_profit = assets.aggregate(total_profit=Sum('profit'))['total_profit'] or 0
        assets = list(assets)
        for asset in assets: #Добавление поля с полный прибылью каждого актива после запроса к бд
            asset['profit_asset'] = culculate_asset_profit(asset['portfolio_id'], asset['asset_id'])
        balance = (Portfolio.objects.get(id=portfolio_id)).balance
        profit = culculate_profit(portfolio_id)

    portfolios = Portfolio.objects.filter(user=request.user)
    data = {'assets': assets,
        'portfolios': portfolios,
        'selected': portfolio_id,
        'total_profit': total_profit,
        'balance': balance,
        'profit': profit}
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
def detail(request, portfolio_id, asset_id):
    deals = Deal.objects.filter(asset_id=asset_id, portfolio_id=portfolio_id, portfolio__user=request.user)
    asset = Asset.objects.get(id=asset_id)
    payments = Payment.objects.filter(asset_id=asset_id, portfolio_id=portfolio_id, portfolio__user=request.user)
    data = {'deals': deals, 'portfolio_id': portfolio_id, 'asset_id': asset_id, 'asset': asset, 'payments': payments}
    return render(request, 'portfolio/detail.html', data)