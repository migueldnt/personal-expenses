from django.db import models

from django.utils.timezone import now as now_for_default
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='accounts',null=True)
    balance = models.FloatField(default=0)
    type_account = models.CharField(max_length=20, choices=[("normal","Normal"),("debt","Debt")],default="normal")
    order = models.IntegerField(default=0)
    created = models.DateTimeField(default=now_for_default)
    

class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.FloatField(default=0)
    account = models.ForeignKey(Account, models.DO_NOTHING,related_name="transactions")
    occurred_in = models.DateTimeField(default=now_for_default)
    created = models.DateTimeField(default=now_for_default)
    type_transaction = models.CharField(max_length=20, choices=[("add","Add"),("subtract","Subtract")])

