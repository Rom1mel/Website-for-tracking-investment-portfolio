from django.db import transaction
from deals.models import Payment
from portfolio.models import PortfolioAsset, Price, Portfolio
from django.core.exceptions import ValidationError
from django.db.models import OuterRef, Subquery, F

@transaction.atomic
def new_payment(payment):
    type = payment.type
    portfolio = payment.portfolio
    asset = payment.asset
    value = payment.value
    exsist = PortfolioAsset.objects.filter(portfolio=portfolio, asset=asset).exists()
    if not exsist:
        raise ValidationError("Актив не принадлежит выбранному портфелю.")
    else:
        if type == 'accrual':
            portfolio.balance += value
        else:
            if portfolio.balance < value:
                raise ValidationError("Баланс не может стать отрицательным")
            else:
                portfolio.balance -= value
        payment.save()
        portfolio.save()

@transaction.atomic
def delete_payment_service(pk):
    payment = Payment.objects.get(pk=pk)
    type = payment.type
    portfolio = payment.portfolio
    asset = payment.asset
    value = payment.value
    if type == 'debit':
        portfolio.balance += value
        payment.delete()
        portfolio.save()
    else:
        if portfolio.balance < value:
            raise ValidationError("Баланс не может стать отрицательным")
        else:
            portfolio.balance -= value
            payment.delete()
            portfolio.save()