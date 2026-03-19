from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    else:
        return redirect('login')
def register(request):
    return render(request, 'registration/register.html')