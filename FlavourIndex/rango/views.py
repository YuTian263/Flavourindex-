from django.shortcuts import redirect, render
from forms import UserRegistrationForm

# Create your views here.
def register(request): 
    if request.method == "POST":
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form}) 