from django.contrib import admin
from django.contrib.sessions.models import Session

from . models import *

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'time_stamp']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'name', 'count', 'portfolio']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'portfolio', 'asset', 'value']