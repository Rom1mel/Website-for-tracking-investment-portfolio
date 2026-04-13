from django.db import transaction
from deals.models import Receipt
from portfolio.models import PortfolioAsset, Price, Portfolio
from django.core.exceptions import ValidationError
from django.db.models import OuterRef, Subquery, F

@transaction.atomic
def new_receipt(receipt):
    portfolio = receipt.portfolio
    if receipt.type == 'add':
        portfolio.balance += receipt.value
    else:
        if portfolio.balance < receipt.value:
            raise ValidationError('Нельзя вывести больше, чем есть на балансе')
        else:
            portfolio.balance -= receipt.value
    portfolio.save()
    receipt.save()

@transaction.atomic
def delete_receipt_service(pk):
    receipt = Receipt.objects.get(pk=pk)
    portfolio = receipt.portfolio
    if receipt.type == 'withdraw':
        portfolio.balance += receipt.value
    else:
        if portfolio.balance < receipt.value:
            raise ValidationError('Действие приведёт к отрицательному балансу')
        else:
            portfolio.balance -= receipt.value
    portfolio.save()
    receipt.delete()