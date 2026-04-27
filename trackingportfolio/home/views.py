from django.shortcuts import render, redirect
from django.http import HttpResponse
from  portfolio.models import Price, Asset
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect('login')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})