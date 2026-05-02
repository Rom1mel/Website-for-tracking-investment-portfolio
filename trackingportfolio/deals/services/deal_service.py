from django.db import transaction
from deals.models import Deal
from portfolio.models import PortfolioAsset, Portfolio
from django.core.exceptions import ValidationError

@transaction.atomic
def new_deal(deal, is_save):
    portfolio = deal.portfolio
    asset = deal.asset
    count = deal.value
    price = deal.price_per_unit
    operation = deal.type
    asset_exsists = PortfolioAsset.objects.filter(portfolio=portfolio, asset=asset).first()
    if asset_exsists:
        if operation == 'buy':
            if count * price > portfolio.balance:
                raise ValidationError('Недостаточно баланса для покупки')
            portfolio.balance -= count * price
            asset_exsists.price = (asset_exsists.price * asset_exsists.count + count * price) / (
                        asset_exsists.count + count)
            asset_exsists.count += count
            asset_exsists.save()
        elif operation == 'sell' and count <= asset_exsists.count:
            portfolio.balance += count * price
            asset_exsists.count -= count
            if asset_exsists.count == 0:
                asset_exsists.delete()
            else:
                asset_exsists.save()
        else:
            raise ValidationError("Недостаточно актива для продажи")
    else:
        if operation == 'buy':
            if count * price > portfolio.balance:
                raise ValidationError('Недостаточно баланса для покупки')
            portfolio.balance -= count * price
            PortfolioAsset.objects.create(portfolio=portfolio, asset=asset, count=count, price=price)
        else:
            raise ValidationError("Недостаточно актива для продажи")
    portfolio.save()
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
    delete_deal(old_deal.id)
    new_deal(deal, True)

@transaction.atomic
def delete_deal(pk):
    deal = Deal.objects.get(pk=pk)
    deal_portfolio = deal.portfolio
    if deal.type == 'buy':
        deal_portfolio.balance += deal.value * deal.price_per_unit
    else:
        if deal_portfolio.balance < deal.value * deal.price_per_unit:
            raise ValidationError('Баланс станет отрицательным при этом действии')
        else:
            deal_portfolio.balance -= deal.value * deal.price_per_unit
    deal.delete()
    deal_portfolio.save()
    recalculate_portfolio(deal_portfolio)