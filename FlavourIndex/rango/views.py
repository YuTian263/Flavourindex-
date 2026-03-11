from email import message

from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
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

def index(request):
    return render(request, "index.html")    

def add_receipe(request):
    if request.method == "POST": 
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe added successfully.")
            return redirect("index")
    else:
        form = RecipeForm()
    return render(request, "add_receipe.html", {"form": form})