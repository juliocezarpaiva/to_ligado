from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class UserQuotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    symbol = models.CharField(max_length=10)
    update_interval = models.IntegerField()
    higher_limit = models.FloatField()
    lower_limit = models.FloatField()
    notification_check = models.BooleanField(default=False)