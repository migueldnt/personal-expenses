from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponseRedirect,  HttpResponseForbidden, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


from .forms import AccountForm,TransactionForm,EditAccountForm
from .models import Account,Transaction

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
def homeCapture(request):
    if request.user.is_authenticated:
        accounts = Account.objects.filter(user=request.user,status="visible").order_by("order")
        accounts_json = serializers.serialize("json",accounts)
        active_account = request.GET["account-active"] if "account-active" in request.GET else 0 
        return render(request=request,template_name="cuentas/home.html",
            context={"accounts":accounts_json,"active_account":active_account,"user":request.user}
            )
    
    return redirect("login")

@login_required
def createAccount(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        
        #print(form.is_valid(), request.user.id,"is valid")
        if form.is_valid():
            account=form.save()
            account.user = request.user
            next_order = Account.objects.filter(user=request.user).count() + 1
            account.order = next_order
            account.save()
            return HttpResponseRedirect("/?account-active="+str(account.id))
        else:
           return render(request=request,template_name="cuentas/form_account.html",context={"form":form, "title":"Error al guardar, vuelve a intentarlo"}) 
    
    form = AccountForm()
    return render(request=request,template_name="cuentas/form_account.html",context={"form":form,"title":"Crear nueva cuenta"})

@login_required
def editAccount(request,account_id):
    account_to_edit = get_object_or_404(Account,pk=account_id,user=request.user)
    #print(account_to_edit)
    if request.method == 'POST':
        form = EditAccountForm(request.POST,instance=account_to_edit)
        
        #print(form.is_valid(), request.user.id,"is valid")
        if form.is_valid():
            account=form.save()
            #account.user = request.user
            #next_order = Account.objects.filter(user=request.user).count() + 1
            #account.order = next_order
            #account.save()
            return HttpResponseRedirect("/?account-active="+str(account.id))
        else:
           return render(request=request,template_name="cuentas/form_account.html",context={"form":form, "title":"Error al guardar, vuelve a intentarlo"}) 
    
    form = EditAccountForm(instance=account_to_edit)
    return render(request=request,template_name="cuentas/form_account.html",context={"form":form,"title":"Modificando cuenta"})

@login_required
def allAccounts(request):
    accounts = Account.objects.filter(user=request.user).order_by("order")
    return render(request=request,template_name="cuentas/all_accounts.html",context={"accounts":accounts})

@login_required
def createTransaction(request) :
    """
    Guarda una nueva transaccion
    Si se desea crear una vista para modificar una transaccion ya existente crear otra pf
    """
    formTransaction = TransactionForm(request.POST)
    if request.method == "POST" and  formTransaction.is_valid() :
        
        #print(formTransaction)
        ##en el form lo que se manda como id de otro objeto foraneo ya en el formulario es el objeto,
        #se debe acceder a sus propiedades
        id_account = formTransaction.cleaned_data["account"].pk
        #print(id_account)
        es_cuenta_propia=Account.objects.filter(user=request.user,pk=id_account).exists()
        #print(id_account, es_cuenta_propia,"Usuario modificando ...")

        if  es_cuenta_propia:
            transaction = formTransaction.save()
            
            id_saved_transaction = transaction.pk
            account_primer_target = transaction.account
            amount_primer_target = transaction.amount
            tipo_primer_target = transaction.type_transaction

            transaction.amount = abs(transaction.amount) if tipo_primer_target == "add" else -abs(transaction.amount)
            transaction.save()

            #checar si la transaccion es relaccionada y modifica a otra cuenta
            modifico_2_cuentas = False
            dict_2da_cuenta = {}
            if transaction.affected_account_id!=0 and Account.objects.filter(pk=transaction.affected_account_id).exists():
                print(transaction.account, "se va a guardar en dos cuentas!!")
                tipo = "add" if  transaction.type_transaction =="subtract" else "subtract"
                #crear otra transaccion para la cuenta relacionada
                transaction.pk = None
                account_2target= Account.objects.get(pk=transaction.affected_account_id)
                transaction.account =account_2target
                transaction.type_transaction = tipo
                transaction.amount = abs(transaction.amount) if tipo == "add" else -abs(transaction.amount)
                transaction.related_transaction_id = id_saved_transaction
                transaction.affected_account_id = account_primer_target.pk
                transaction.save()

                id_transaction2 = transaction.pk
                transaction_target1 = Transaction.objects.get(pk=id_saved_transaction)
                transaction_target1.related_transaction_id = id_transaction2
                transaction_target1.save()

                account_2target.balance = account_2target.balance + abs(transaction.amount) if tipo == "add" else  account_2target.balance - abs(transaction.amount)
                account_2target.save()

                modifico_2_cuentas = True
                dict_2da_cuenta["id"] = id_transaction2
                dict_2da_cuenta["account_balance"] = account_2target.balance
                dict_2da_cuenta["account_id"] = account_2target.pk



            #modificar la cuenta para generar nuevos saldos
            account_primer_target.balance = account_primer_target.balance + abs(amount_primer_target) if tipo_primer_target == "add" else  account_primer_target.balance - abs(amount_primer_target)
            account_primer_target.save()

            response={"status":True, "saved_transaction":
                {"id":id_saved_transaction, "account_balance":  account_primer_target.balance, "account_id":account_primer_target.pk } }
            if modifico_2_cuentas:
                response["related_transaction"]  = dict_2da_cuenta           

            return JsonResponse(response)
        else:
            return HttpResponseForbidden()

            
    else:
        #return JsonResponse({"status":True, "ddd1":"dddd"})

        return HttpResponseForbidden()


@login_required
def transactionsByAccount(request,account_id):
    account_obj = get_object_or_404(Account,pk=account_id,user=request.user)
    queryset_trans = Transaction.objects.filter(account=account_obj).order_by("-occurred_in")
    transactions = get_list_or_404(queryset_trans)
    transactions_json = serializers.serialize("json",transactions)
    return render(request=request,template_name="cuentas/transactions_by_account.html",
        context={"transactions":transactions_json,"account":account_obj})
