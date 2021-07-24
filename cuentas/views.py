from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.core import serializers

from .forms import AccountForm
from .models import Account

def homeCapture(request):
    if request.user.is_authenticated:
        accounts = Account.objects.filter(user=request.user)
        accounts_json = serializers.serialize("json",accounts)
        active_account = request.GET["account-active"]
        return render(request=request,template_name="cuentas/home.html",
            context={"accounts":accounts_json,"active_account":active_account}
            )
    
    return redirect("login")

def createAccount(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        
        print(form.is_valid(), request.user.id,"is valid")
        if form.is_valid():
            account=form.save()
            account.user = request.user
            account.save()
            return HttpResponseRedirect("/?account-active="+str(account.id))
        else:
           return render(request=request,template_name="cuentas/create_account.html",context={"form":form, "status":"failed"}) 
    
    form = AccountForm()
    return render(request=request,template_name="cuentas/create_account.html",context={"form":form,"status":"ok"})