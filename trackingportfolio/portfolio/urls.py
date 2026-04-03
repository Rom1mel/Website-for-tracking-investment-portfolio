from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('add/', include('deals.urls')),
    path('create_portfolio/', views.create_portfolio, name='create_portfolio'),
]