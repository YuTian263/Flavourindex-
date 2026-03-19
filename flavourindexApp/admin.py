from django.contrib import admin
from flavourindexApp.models import FoodCategory, Recipe

# Register your models here.
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'foodCategory', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)