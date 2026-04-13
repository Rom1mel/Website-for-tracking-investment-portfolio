from django.urls import path
from . import views

urlpatterns = [
    path('', views.history, name='history'),
    path('add/', views.add, name='add'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('add_payment', views.add_payment, name='add_payment'),
    path('delete_payment/<int:pk>/', views.delete_payment, name='delete_payment'),
]