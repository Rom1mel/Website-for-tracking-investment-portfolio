from django.shortcuts import render, redirect
from portfolio.models import PortfolioAsset, Portfolio, Asset
from deals.services.deal_service import new_deal, update_deal, delete_deal
from deals.services.payment_service import new_payment, delete_payment_service
from deals.services.receipt_service import new_receipt, delete_receipt_service
from django.db.models import Q
from .forms import *
from django.http import JsonResponse



def history(request):
    portfolio_id = request.GET.get('portfolio_id', 'all')
    if portfolio_id == 'all':
        deals = Deal.objects.filter(portfolio__user=request.user)
        payments = Payment.objects.filter(portfolio__user=request.user)
        receipts = Receipt.objects.filter(portfolio__user=request.user)
    else:
        deals = Deal.objects.filter(portfolio_id=portfolio_id, portfolio__user=request.user)
        payments = Payment.objects.filter(portfolio_id=portfolio_id, portfolio__user=request.user)
        receipts = Receipt.objects.filter(portfolio_id=portfolio_id, portfolio__user=request.user)
    portfolios = Portfolio.objects.filter(user=request.user)
    data = {'deals': deals, 'portfolios': portfolios, 'selected': portfolio_id, 'payments': payments, 'receipts': receipts}
    return render(request, 'deals/history.html', data)

def add(request):
    show_all = request.GET.get('all') == '1'
    if request.method == 'POST':
        form = DealForm(request.POST, user = request.user, show_all = show_all)
        if form.is_valid():
            deal = form.save(commit=False)
            new_deal(deal, True)
        return redirect('history')
    else:
        form = DealForm(user = request.user, show_all = show_all)
        return render(request, 'deals/add.html', {'form': form, 'show_all': show_all})

def search(request):
    query = request.GET.get("q", "")
    asset_type = request.GET.get("type", "")

    assets = Asset.objects.all()

    if asset_type:
        assets = assets.filter(type=asset_type)

    if query:
        assets = assets.filter(
            Q(name__icontains=query) |
            Q(ticker__icontains=query)
        )

    assets = assets.order_by("name")[:30]

    results = []

    for asset in assets:
        results.append({
            "id": asset.id,
            "text": f"{asset.name} ({asset.ticker})",
        })

    return JsonResponse({
        "results": results
    })

def edit(request, pk):
    deal = Deal.objects.get(id = pk,portfolio__user = request.user)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal, user=request.user)
        if form.is_valid():
            deal = form.save(commit=False)
            update_deal(deal,pk)
        return redirect('history')
    else:
        form = DealForm(instance = deal, user=request.user)
        return render(request, 'deals/edit.html', {'form': form})

def delete(request, pk):
    deal = Deal.objects.get(id = pk,portfolio__user = request.user)
    if request.method == 'POST':
        delete_deal(pk)
        return redirect('history')
    else:
        return render(request, 'deals/delete.html', {'deal': deal})

def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user = request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            new_payment(payment)
        return redirect('history')
    else:
        form = PaymentForm(user = request.user)
        return render(request, 'deals/add_payment.html', {'form': form})

def delete_payment(request, pk):
    payment = Payment.objects.get(id = pk, portfolio__user = request.user)
    if request.method == 'POST':
        delete_payment_service(pk)
        return redirect('history')
    else:
        return render(request, 'deals/delete_payment.html', {'payment': payment})

def add_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST, user=request.user)
        if form.is_valid():
            receipt = form.save(commit=False)
            new_receipt(receipt)
        return redirect('history')
    else:
        form = ReceiptForm(user=request.user)
        return render(request, 'deals/add_receipt.html', {'form': form})
def delete_receipt(request, pk):
    receipt = Receipt.objects.get(id = pk)
    if request.method == 'POST':
        delete_receipt_service(pk)
        return redirect('history')
    else:
        return render(request, 'deals/delete_receipt.html', {'receipt': receipt})
