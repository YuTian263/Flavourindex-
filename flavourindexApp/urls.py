from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from flavourindexApp import views
from . import views

app_name = 'flavourindexApp'

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("add-recipe/", views.add_recipe, name="add_recipe"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("register/", views.register, name="register"),
    path("api/recipes/", views.recipe_list_api, name="recipe_list_api"),
]

