from email import message

from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

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
def post_recipe(request):
    if request.method == "POST": 
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe added successfully.")
            return redirect("home")
    else:
        form = RecipeForm()
    return render(request, "flavourindex/post_receipe.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('flavourindexApp:home'))
