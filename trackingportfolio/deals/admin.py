from django.contrib import admin
from . models import *

@admin.register(Deal)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'portfolio', 'asset', 'value']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['type', 'portfolio', 'asset', 'value']

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['type', 'portfolio', 'value']