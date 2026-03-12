from django.contrib import admin
from flavourindexApp.models import FoodCategory, Recipe

# Register your models here.
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'foodCategory', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)