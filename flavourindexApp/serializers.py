from rest_framework import serializers
from .models import Recipe  # your Recipe model

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # returns author username

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'category', 'image', 'author']