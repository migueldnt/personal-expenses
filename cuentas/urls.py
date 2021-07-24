from django.urls import path,include

from .views import homeCapture,createAccount

urlpatterns=[
    path("",homeCapture,name="home"),
    path("create-account/",createAccount,name="create_account"),
    #path("edit-account/",createAccount,name="edit_account")
]