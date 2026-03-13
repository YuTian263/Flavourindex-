from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "flavourindexApp"


urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("add-recipe/", views.add_recipe, name="add_recipe"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", next_page='/'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register, name="register"),
    path("api/recipes/", views.recipe_apis, name="recipe_api"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
