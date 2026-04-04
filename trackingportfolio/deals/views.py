from django.shortcuts import render, redirect
from portfolio.forms import DealForm
from portfolio.models import PortfolioAsset, Portfolio
from .models import Deal
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
            portfolio = deal.portfolio
            asset = deal.asset
            count = deal.value
            price = deal.price_per_unit
            operation = deal.type
            asset_exsists = PortfolioAsset.objects.filter(portfolio = portfolio, asset = asset).first()
            error = False
            if asset_exsists:
                if operation == 'buy':
                    asset_exsists.price = (asset_exsists.price * asset_exsists.count + count * price)/(asset_exsists.count + count)
                    asset_exsists.count += count
                    asset_exsists.save()
                elif operation == 'sell' and count <= asset_exsists.count:
                    asset_exsists.count -= count
                    if asset_exsists.count == 0:
                        asset_exsists.delete()
                    else:
                        asset_exsists.save()
                else:
                    form.add_error(None, "Ошибка продажи")
                    error = True

            else:
                if operation == 'buy':
                    PortfolioAsset.objects.create(portfolio = portfolio, asset = asset, count = count, price = price)
                else:
                    form.add_error(None, "Ошибка продажи")
                    error = True
            if not error:
                deal.save()

        return redirect('history')
    else:
        form = DealForm(user = request.user, show_all = show_all)
        return render(request, 'deals/add.html', {'form': form, 'show_all': show_all})

def edit(request): # ← добавить
    return render(request, 'deals/edit.html')

