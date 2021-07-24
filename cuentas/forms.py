from django import forms
from django.db.models import fields
from .models import Account
from django.forms import TextInput,HiddenInput

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields =["id","name","type_account"]
        
