from django.contrib import admin

from . models import *

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'time_stamp']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ticker']
    list_display = ['ticker', 'name', 'type']

@admin.register(PortfolioAsset)
class PortfolioAssetAdmin(admin.ModelAdmin):
    autocomplete_fields = ['asset']
    list_display = ['portfolio', 'asset', 'count', 'price']