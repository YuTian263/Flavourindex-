from email import message

from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def home(request):
    response = render(request, 'flavourindex/home.html')
    return response

def register(request): 
    if request.method == "POST":
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "flavourindex/register.html", {"form": form})    

@login_required
def add_recipe(request):
    if request.method == "POST": 
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe added successfully.")
            return redirect("home")
    else:
        form = RecipeForm()
    return render(request, "flavourindex/add_receipe.html", {"form": form})



def index(request):
    return render(request, "index.html")

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



