from django.urls import path, include

from .views import deleteTransaction, homeCapture, createAccount, editAccount, allAccounts, createTransaction, transactionsByAccount, editTransaction, deleteTransaction

urlpatterns = [
    path("", homeCapture, name="home"),
    path("create-account/", createAccount, name="create_account"),
    path("edit-account/<int:account_id>/", editAccount, name="edit_account"),
    path("all-accounts/", allAccounts, name="all_accounts"),
    path("rest/create-transaction/", createTransaction, name="create_transaction"),
    path("transactions/<int:account_id>/", transactionsByAccount, name="list_transactions"),
    path("edit-transaction/<int:transaction_id>/", editTransaction, name="edit_transaction"),
    path("delete-transaction/<int:transaction_id>/", deleteTransaction, name="delete_transaction"),

]
