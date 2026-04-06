from django.shortcuts import render, redirect
from portfolio.forms import DealForm
from portfolio.models import PortfolioAsset, Portfolio
from .models import Deal
from deals.services.deal_service import new_deal, update_deal, delete_deal
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView



def history(request):
    portfolio_id = request.GET.get('portfolio_id', 'all')
    if portfolio_id == 'all':
        deals = Deal.objects.filter(portfolio__user=request.user)
    else:
        deals = Deal.objects.filter(portfolio_id=portfolio_id, portfolio__user=request.user)
    portfolios = Portfolio.objects.filter(user=request.user)
    data = {'deals': deals, 'portfolios': portfolios, 'selected': portfolio_id}
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

def edit(request, pk):
    deal = Deal.objects.get(id = pk,portfolio__user = request.user)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            deal = form.save(commit=False)
            update_deal(deal,pk)
        return redirect('history')
    else:
        form = DealForm(instance = deal)
        return render(request, 'deals/edit.html', {'form': form})

def delete(request, pk):
    deal = Deal.objects.get(id = pk,portfolio__user = request.user)
    if request.method == 'POST':
        delete_deal(pk)
        return redirect('history')
    else:
        return render(request, 'deals/delete.html', {'deal': deal})
