from django.shortcuts import render

def history(request):
    return render(request, 'deals/history.html')

def add(request):
    return render(request, 'deals/add.html')

def edit(request):
    return render(request, 'deals/edit.html')

