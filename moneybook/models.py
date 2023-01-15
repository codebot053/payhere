from django.db import models
from django.conf import settings

class MoneyBook(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash_amount = models.IntegerField(default=0)
    latest_log_id = models.IntegerField(default=0)
