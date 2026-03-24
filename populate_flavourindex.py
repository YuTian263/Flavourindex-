import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'FlavourIndexProject.settings')

import django
django.setup()
from flavourindexApp.models import FoodCategory, Recipe

def populate():
    breakfast_recipes = [
        {
            'title': 'Maple Pancakes',
            'description': 'Stunning breakfast pancake stack to set you up for the day!',
            'ingredients': 'Flour, eggs, butter, milk, syrup, bacon',
            'instructions': 'Make batter, flip while cooking' },
        {
            'title': 'Full English',
            'description': 'Classic cooked breakfast',
            'ingredients': 'Sausages, bacon, eggs, tomato, mushrooms',
            'instructions': 'Cook sausages, bacon, tomato and mushrooms in oven, fry eggs in pan'} ]
    
    lunch_recipes = [
        {
            'title': 'Chicken Wrap',
            'description': 'Wonderful chicken wrap to keep you going at work',
            'ingredients': 'Tortilla wrap, chicken, lettuce, cheese',
            'instructions': 'Fry chicken, add to tortilla, wrap tighly'},
        {
            'title': 'Caeasar Salad',
            'description': 'Delightful salad to enjoy a light lunch',
            'ingredients': 'Lettuce, croutons, chicken, bacon, dressing',
            'instructions': 'Cook chicken and bacon, add ingredients to bowl, mix'} ]
    
    dinner_recipes = [
        {
            'title': 'Margarita Pizza',
            'description': 'Cheese and mozzarella pizza for a quick easy dinner',
            'ingredients': 'dough, tomato sauce, mozzarella',
            'instructions': 'Spread sauce across dough, sprinkle cheese on top, cook in oven' },
        {
            'title': 'Double Cheeseburger',
            'description': 'Delicious double cheeseburger for proper hearty meal',
            'ingredients': 'bun, burger patty, tomato, lettuce, cheese',
            'instructions': 'Cook burger patty, assemble burger' } ]
    
    dessert_recipes = [
        {
            'title': 'Sticky Toffee Pudding',
            'description': 'Lovely sticky toffee pudding, perfect dessert',
            'ingredients': 'butter, sugar, eggs, flour, treacle, milk',
            'instructions': 'Combine butter, sugar, eggs, flour, add milk, melt butter in pan and add sugar and treacle for sauce, bake pudding in oven, cover with sauce'
        } ]
    
    cats = {
        'Breakfast': breakfast_recipes,
        'Lunch': lunch_recipes,
        'Dinner': dinner_recipes,
        'Dessert': dessert_recipes
    }

    for cat_name, recipes in cats.items():
        cat = add_foodCategory(cat_name)
        for r in recipes:
            add_recipe(cat, r['title'], r['description'], r['ingredients'], r['instructions'])

    #Print results
    for c in FoodCategory.objects.all():
        print(f'Category: {c.name}')
        for r in Recipe.objects.filter(foodCategory=c):
            print(f'-Recipe: {r.title}')

def add_recipe(cat, title, description, ingredients, instructions):
    r = Recipe.objects.get_or_create(foodCategory=cat, title=title)[0]
    r.description = description
    r.ingredients = ingredients
    r.instructions = instructions
    r.save()
    return r

def add_foodCategory(name):
    f = FoodCategory.objects.get_or_create(name=name)[0]
    return f

#execute
if __name__ == '__main__':
    print('Starting FlavourIndex population script...')
    populate()