from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from rango import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/login", auth_views.LoginView.as_view(template_name = "login.html"), name="login"),
    path("accounts/logout", auth_views.LogoutView.as_view(template_name = "logout.html"), name="logout"),
    path("accounts/register", views.register, name="register"),
]

