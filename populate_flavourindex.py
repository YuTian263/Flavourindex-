import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'FlavourIndexProject.settings')

import django
django.setup()
from flavourindexApp.models import FoodCategory, Recipe
from django.core.files import File

def populate():
    breakfast_recipes = [
        {
            'title': 'Maple Pancakes',
            'description': 'Stunning breakfast pancake stack to set you up for the day!',
            'ingredients': 'Flour\neggs\nbutter\nmilk\nsyrup\nbacon',
            'instructions': 'Make batter\nflip while cooking',
            'picture': 'recipes/pancakes.jpg' },
        {
            'title': 'Full English',
            'description': 'Classic cooked breakfast',
            'ingredients': 'Sausages\nbacon\neggs\ntomato\nmushrooms',
            'instructions': 'Cook sausages\nbacon\ntomato and mushrooms in oven\nfry eggs in pan',
            'picture': 'recipes/full_english.jpg'} ]
    
    lunch_recipes = [
        {
            'title': 'Chicken Wrap',
            'description': 'Wonderful chicken wrap to keep you going at work',
            'ingredients': 'Tortilla wrap\nchicken\nlettuce\ncheese',
            'instructions': 'Fry chicken\nadd chicken, lettuce, and cheese to tortilla\nwrap tighly',
            'picture': 'recipes/wrap.jpg'},
        {
            'title': 'Caeasar Salad',
            'description': 'Delightful salad to enjoy a light lunch',
            'ingredients': 'Lettuce\ncroutons\nchicken\nbacon\ndressing',
            'instructions': 'Cook chicken and bacon\nadd ingredients to bowl\nmix',
            'picture': 'recipes/caesar_salad.jpg'} ]
    
    dinner_recipes = [
        {
            'title': 'Margarita Pizza',
            'description': 'Cheese and mozzarella pizza for a quick easy dinner',
            'ingredients': 'dough\ntomato sauce\nmozzarella',
            'instructions': 'Spread sauce across dough\nsprinkle cheese on top\ncook in oven',
             'picture': 'recipes/pizza.avif' },
        {
            'title': 'Double Cheeseburger',
            'description': 'Delicious double cheeseburger for proper hearty meal',
            'ingredients': 'bun, burger patty\ntomato\nlettuce\ncheese',
            'instructions': 'Cook burger patty\nassemble burger', 
            'picture': 'recipes/double_cheeseburger.jpg'} ]
    
    dessert_recipes = [
        {
            'title': 'Sticky Toffee Pudding',
            'description': 'Lovely sticky toffee pudding, perfect dessert',
            'ingredients': 'butter\nsugar\neggs\nflour\ntreacle\nmilk',
            'instructions': 'Combine butter\nsugar\neggs\nflour\nadd milk\nmelt butter in pan and add sugar and treacle for sauce\nbake pudding in oven\ncover with sauce', 
            'picture': 'recipes/sticky_toffee_pudding.jpg' } ]
    
    snack_recipes = [
        {
            'title': 'Sliders',
            'description': 'Mini burgers, great as a snack between meals or when hosting',
            'ingredients': 'mini burger buns\nmini burgers\nlettuce\ntomato\nonion\ncheese',
            'instructions': 'Cook mini burgers in pan/oven\nplace cheese on a minute before cooked\ntoast buns\nassemble',
            'picture': 'recipes/sliders.jpg'} ]
    
    drink_recipes = [
        {
            'title': 'Mojito',
            'description': 'Amazing cocktail, great for drinks with friends!!!',
            'ingredients': 'mint leaves\nlime juice\nrum\nsoda water\nice\nsugar',
            'instructions': 'muddle mint, lime juice and sugar\nadd rum\nadd ice and stir until sugar dissolved\ntop with soda water\ngarnish with mint leaves',
            'picture': 'recipes/mojito.jpg'}  ]

    cats = {
        'Breakfast': breakfast_recipes,
        'Lunch': lunch_recipes,
        'Dinner': dinner_recipes,
        'Dessert': dessert_recipes,
        'Snack': snack_recipes,
        'Drink': drink_recipes
    }

    for cat_name, recipes in cats.items():
        cat = add_foodCategory(cat_name)
        for r in recipes:
            add_recipe(cat, r['title'], r['description'], r['ingredients'], r['instructions'], r['picture'])

    #Print results
    for c in FoodCategory.objects.all():
        print(f'Category: {c.name}')
        for r in Recipe.objects.filter(foodCategory=c):
            print(f'-Recipe: {r.title}')

def add_recipe(cat, title, description, ingredients, instructions, image_path=None):
    r = Recipe.objects.get_or_create(foodCategory=cat, title=title)[0]
    r.description = description
    r.ingredients = ingredients
    r.instructions = instructions
    if image_path:
        image_complete_path = os.path.join('media', image_path)
        with open(image_complete_path, 'rb') as f:
            r.picture.save(os.path.basename(image_complete_path), File(f), save=False)

    r.save()
    return r

def add_foodCategory(name):
    f = FoodCategory.objects.get_or_create(name=name)[0]
    return f

#execute
if __name__ == '__main__':
    print('Starting FlavourIndex population script...')
    populate()