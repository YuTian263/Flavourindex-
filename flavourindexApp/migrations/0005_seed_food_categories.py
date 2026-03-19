# Updated Migration so that the populate script doesn't need to be run every time

from django.db import migrations

def seed_categories(apps, schema_editor):
    FoodCategory = apps.get_model('flavourindexApp', 'FoodCategory')
    categories = ['Breakfast', 'Lunch', 'Dinner']
    for name in categories:
        FoodCategory.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('flavourindexApp', '0004_recipe_created_by_alter_foodcategory_id_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories),
    ]