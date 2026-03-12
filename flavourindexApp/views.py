from email import message
from .models import Recipe
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, RecipeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

from flavourindexApp.models import Recipe

# Create your views here.

def home(request):
    response = render(request, 'flavourindex/home.html')
    return response

def view_recipes(request):
    recipes_list = Recipe.objects.all().order_by('title')
    

def register(request): 
    if request.method == "POST":
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})    


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)

            if hasattr(recipe, "created_by"):
                recipe.created_by = request.user

            recipe.save()
            messages.success(request, "Recipe published successfully!")
            return redirect("flavourindexApp:index")
        else:
            print("FORM ERRORS:", form.errors)
            messages.error(request, "Recipe could not be published. Please fix the errors below.")
    else:
        form = RecipeForm()

    return render(request, "add_recipe.html", {"form": form})

def post_recipe(request):
    if request.method == "POST": 
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe added successfully.")
            return redirect("home")
    else:
        form = RecipeForm()
    return render(request, "add_receipe.html", {"form": form})



def index(request):
    recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe_detail.html", {"recipe": recipe})


def recipe_list_api(request):
    recipes = Recipe.objects.all()

    data = []
    for recipe in recipes:
        data.append({
            "id": recipe.id,
            "name": recipe.name,
            "ingredients": recipe.ingredients,
            "instructions": recipe.instructions,
        })

    return JsonResponse(data, safe=False)




    return render(request, "flavourindex/post_receipe.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('flavourindexApp:home'))

#Temp so migrations can be made (Unaable to migrate without this as recently_viewed had a url path but no view)
def recently_viewed(request):
    return render(request, 'recently_viewed.html')