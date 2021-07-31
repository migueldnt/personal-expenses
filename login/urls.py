from os import name
from django.urls import path, include

from django.contrib.auth import views as auth_views
from .views import registroView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login/login.html",redirect_field_name="next",redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="login/logout.html"), name="logout"),
    path("change-password/", auth_views.PasswordChangeView.as_view(template_name="login/change-password.html") ,name="password_change"),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="login/password-done.html"),name="password_change_done" ),
    path("registro/",registroView, name="registro_usuario")
]
