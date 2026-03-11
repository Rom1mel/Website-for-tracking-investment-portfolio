from django.contrib.auth.models import User
from django.db import models

class Sessions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    duration = models.PositiveIntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True)