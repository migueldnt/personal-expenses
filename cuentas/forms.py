from django import forms
from django.db.models import fields
from .models import Account,Transaction
from django.forms import TextInput,HiddenInput

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields =["id","name","type_account"]

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields =["id","name","type_account","comments","order","status"]
        


class TransactionForm(forms.ModelForm):
    """
    Si se va a acupar otro form para editar la transaccion (de sugerencia que se opupe este) 
    renombrar esta clase a NewTransactionForm
    """
    class Meta:
        model = Transaction
        fields = ["id","amount","concept","account","occurred_in","affected_account_id","type_transaction"]