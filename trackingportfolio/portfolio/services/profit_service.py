from django.db import transaction
from deals.models import Payment, Receipt, Deal
from portfolio.models import PortfolioAsset, Price
from django.core.exceptions import ValidationError
from django.db.models import OuterRef, Subquery, F
from portfolio.models import Portfolio, Asset


def culculate_profit(pk):
    portfolio = Portfolio.objects.get(id=pk)
    price = Price.objects.filter(asset=OuterRef('asset')).values('price')
    all_assets = PortfolioAsset.objects.filter(portfolio=portfolio).values('count').annotate(current_price=Subquery(price))
    profit = portfolio.balance
    for asset in all_assets:
        profit += asset['current_price'] * asset['count']
    all_replenishments = Receipt.objects.filter(portfolio=portfolio, type='add').values('value')
    all_withdraws = Receipt.objects.filter(portfolio=portfolio, type='withdraw').values('value')
    for replenishment in all_replenishments:
        profit -= replenishment['value']
    for withdraw in all_withdraws:
        profit += withdraw['value']
    return profit

def culculate_asset_profit(portfolio_pk, asset_pk):
    portfolio = Portfolio.objects.get(id=portfolio_pk)
    asset = Asset.objects.get(pk=asset_pk)
    portfolio_asset = PortfolioAsset.objects.filter(asset=asset, portfolio=portfolio).first()
    if not portfolio_asset:
        return 0
    price = (Price.objects.get(asset=portfolio_asset.asset)).price
    profit = portfolio_asset.count * price
    deals = Deal.objects.filter(portfolio=portfolio, asset=asset)
    for deal in deals:
        if deal.type == 'buy':
            profit -= deal.price_per_unit * deal.value
        else:
            profit += deal.price_per_unit * deal.value
    payments = Payment.objects.filter(portfolio=portfolio, asset=asset)
    for payment in payments:
        if payment.type == 'accrual':
            profit += payment.value
        else:
            profit -= payment.value
    return profit