from django.urls import path
from . import views

urlpatterns = [
    path('', views.history, name='history'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
]