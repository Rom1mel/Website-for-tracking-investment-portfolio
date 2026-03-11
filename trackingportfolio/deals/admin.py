from django.contrib import admin
from . models import *

@admin.register(Deal)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'portfolio', 'asset', 'value']
