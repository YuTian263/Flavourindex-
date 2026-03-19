from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea)
    ingredients = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Recipe
        fields = ("title", "description", "ingredients", "instructions", "foodCategory", "picture", "prep_time", "cook_time", "servings", "difficulty")
        
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        ingredients = cleaned_data.get('ingredients')
        instructions = cleaned_data.get('instructions')

        if title and len(title.strip()) < 3:
            self.add_error('title', 'Title must be at least 3 characters long.')

        if description and len(description.strip()) < 10:
            self.add_error('description', 'Description is too short.')

        if ingredients is not None and not ingredients.strip():
            self.add_error('ingredients', 'Ingredients cannot be empty.')

        if instructions is not None and not instructions.strip():
            self.add_error('instructions', 'Instructions cannot be empty.')

        return cleaned_data