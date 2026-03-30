from django.shortcuts import render
from portfolio.forms import PortfolioAssetForm

def history(request):
    return render(request, 'deals/history.html')

def add(request):
    form = PortfolioAssetForm()
    return render(request, 'deals/add.html', {'form': form})

def edit(request): # ← добавить
    return render(request, 'deals/edit.html')

