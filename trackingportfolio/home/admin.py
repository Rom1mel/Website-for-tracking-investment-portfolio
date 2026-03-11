from django.contrib import admin
from . models import *

@admin.register(Sessions)
class SessionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'duration', 'time_stamp')
