from django.db import transaction
from deals.models import Payment
from portfolio.models import PortfolioAsset, Price
from django.core.exceptions import ValidationError
from django.db.models import OuterRef, Subquery, F


@transaction.atomic
def unrealized_profit(portfolio):
    price = Price.objects.filter(asset=OuterRef('asset')).value('price')
    all_assets = PortfolioAsset.objects.filter(portfolio=portfolio).values('count', 'price').annotate(current_price=Subquery(price))
    profit = 0
    for asset in all_assets:
        profit += asset['current_price'] * asset['count'] - asset['price'] * asset['count']
    return profit