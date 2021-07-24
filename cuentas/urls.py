from django.urls import path,include

from .views import homeCapture

urlpatterns=[
    path("",homeCapture,name="home")
]