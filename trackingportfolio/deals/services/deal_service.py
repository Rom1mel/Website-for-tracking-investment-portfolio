from django.db import transaction
from deals.models import Deal
from portfolio.models import PortfolioAsset
from django.core.exceptions import ValidationError

@transaction.atomic
def new_deal(deal, is_save):
    portfolio = deal.portfolio
    asset = deal.asset
    count = deal.value
    price = deal.price_per_unit
    operation = deal.type
    asset_exsists = PortfolioAsset.objects.filter(portfolio=portfolio, asset=asset).first()
    error = False
    if asset_exsists:
        if operation == 'buy':
            asset_exsists.price = (asset_exsists.price * asset_exsists.count + count * price) / (
                        asset_exsists.count + count)
            asset_exsists.count += count
            asset_exsists.save()
        elif operation == 'sell' and count <= asset_exsists.count:
            asset_exsists.count -= count
            if asset_exsists.count == 0:
                asset_exsists.delete()
            else:
                asset_exsists.save()
        else:
            error = True
            raise ValidationError("Недостаточно актива для продажи")
    else:
        if operation == 'buy':
            PortfolioAsset.objects.create(portfolio=portfolio, asset=asset, count=count, price=price)
        else:
            error = True
            raise ValidationError("Недостаточно актива для продажи")
    if is_save:
        deal.save()

@transaction.atomic
def recalculate_portfolio(portfolio):
    PortfolioAsset.objects.filter(portfolio=portfolio).delete()
    deals = Deal.objects.filter(portfolio=portfolio).order_by('id')
    for deal in deals:
        new_deal(deal, False)

@transaction.atomic
def update_deal(deal, pk):
    old_deal = Deal.objects.get(pk=pk)
    old_deal.value = deal.value
    old_deal.price_per_unit = deal.price_per_unit
    old_deal.type = deal.type
    old_deal.asset = deal.asset

    old_deal.save()
    recalculate_portfolio(old_deal.portfolio)

@transaction.atomic
def delete_deal(pk):
    deal = Deal.objects.get(pk=pk)
    deal_portfolio = deal.portfolio
    deal.delete()
    recalculate_portfolio(deal_portfolio)