from django.urls import path, include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login/login.html",redirect_field_name="next"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="login/logout.html"), name="logout")
]
