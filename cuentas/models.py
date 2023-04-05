from django.db import models

from django.utils.timezone import now as now_for_default
from django.contrib.auth.models import User

ACCOUNT_TYPES = [
    ("normal","Normal"), #cuenta que sirve solo para llevar registro, no necesariamente representa una cuenta que tenga el balance actual
    ("debt","Debt"), # cuenta normal de Deuda, para llevar registro de lo que se debe
    ("creditcard","Credit Card"), # Una tarjeta de credito
    ("debitcard","Debit Card") # Una tarjeta de debito
]

# Create your models here.
class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='accounts',null=True)
    balance = models.FloatField(default=0)
    type_account = models.CharField(max_length=20, choices=ACCOUNT_TYPES,default="normal")
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[("visible","Visible"),("hidden","Hidden")], default="visible") 
    created = models.DateTimeField(default=now_for_default)
    comments = models.CharField(max_length=250,default="")
    
    def __str__(self):
        return str(self.user.username)+" ["+self.name + "] $" +str(self.balance)

    def total_transactions(self):
        return self.transactions.count()

class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.FloatField(default=0)
    concept = models.CharField(max_length=250,default="")
    account = models.ForeignKey(Account, models.DO_NOTHING,related_name="transactions")
    occurred_in = models.DateTimeField(default=now_for_default)
    created = models.DateTimeField(default=now_for_default)
    affected_account_id = models.BigIntegerField(default=0)
    related_transaction_id = models.BigIntegerField(default=0)
    type_transaction = models.CharField(max_length=20, choices=[("add","Add"),("subtract","Subtract")])

class AccountMetadata(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.OneToOneField(Account,models.DO_NOTHING,related_name="metadata")
    creditcard_default_cutoffdate = models.SmallIntegerField(default=1)
    creditcard_default_paydeadlinedays = models.SmallIntegerField(default=20)

class AccountMarkers(models.Model):
    id = models.BigAutoField(primary_key=True)
    account =models.ForeignKey(Account,models.DO_NOTHING,related_name="markers")
    date = models.DateTimeField()
    name = models.CharField(max_length=250,default="")
    created = models.DateTimeField(default=now_for_default)
    


class CreditCardArbitrayDates(models.Model):
    """
    Fechas arbitrarias para la tarjeta de credito, solo se permite una de estas por mes
    """
    id = models.BigAutoField(primary_key=True)
    cutoffdate = models.DateField()
    paydeadlinedays = models.DateField()
    accountMetadata = models.ForeignKey(AccountMetadata,models.DO_NOTHING,related_name="creditcard_arbitraydates")