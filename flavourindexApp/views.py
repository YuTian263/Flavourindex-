from email import message
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, RecipeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .services import get_tasty_recipes
from django.db.models import Q
from flavourindexApp.models import Recipe

# Create your views here.
def view_recipes(request):
    recipes_list = Recipe.objects.all().order_by('title')
    

def register(request): 
    if request.method == "POST":
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("flavourindexApp:login")
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
    return render(request, "add_recipe.html", {"form": form})

def index(request):
    return all_recipes(request)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "recipe_detail.html", {"recipe": recipe})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('flavourindexApp:index'))

#Temp so migrations can be made (Unaable to migrate without this as recently_viewed had a url path but no view)
def recently_viewed(request):
    return render(request, 'recently_viewed.html')

#Internal API 
def recipe_apis(request): 
    recipe = Recipe.objects.all()
    data = []
    for r in recipe:
        data.append({
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "category": recipe.foodCategory.name if recipe.foodCategory else None,
            "ingredients": recipe.ingredients,
            "instructions": recipe.instructions,
            "slug": recipe.slug,
            "picture": recipe.picture.url if recipe.picture else None,
        })
    return JsonResponse(data, safe=False)

def all_recipes(request):
    query = request.GET.get("query", "").strip()

    combined = []

    # Local recipes
    local_recipes = Recipe.objects.all()

    if query:
        local_recipes = local_recipes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(foodCategory__name__icontains=query)
        )

    for recipe in local_recipes:
        combined.append({
            "source": "local",
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "image": recipe.picture.url if recipe.picture else None,
            "category": recipe.foodCategory.name if recipe.foodCategory else None,
            "author": getattr(recipe, "author", None),
        })

    # External recipes
    external_recipes = get_tasty_recipes()

    if query:
        external_recipes = [
            recipe for recipe in external_recipes
            if query.lower() in (recipe.get("title") or "").lower()
            or query.lower() in (recipe.get("description") or "").lower()
            or any(query.lower() in tag.lower() for tag in recipe.get("tags", []))
        ]

    for recipe in external_recipes:
        combined.append({
            "source": "external",
            "id": None,
            "title": recipe.get("title"),
            "description": recipe.get("description"),
            "image": recipe.get("picture"),
            "category": ", ".join(recipe.get("tags", [])[:2]) if recipe.get("tags") else None,
            "author": None,
        })

    return render(request, "index.html", {"recipes": combined})