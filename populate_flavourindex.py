import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'FlavourIndexProject.settings')

import django
django.setup()
from flavourindexApp.models import FoodCategory, Recipe
from django.core.files import File
from django.conf import settings
from django.utils.text import slugify

def populate():
    breakfast_recipes = [
        {
            'title': 'Maple Pancakes',
            'description': 'Stunning breakfast pancake stack to set you up for the day!',
            'ingredients': 'Flour\neggs\nbutter\nmilk\nsyrup\nbacon',
            'instructions': 'Make batter\nflip while cooking',
            'picture': 'recipes/pancakes.jpg',
            'prep_time': 40,
            'cook_time': 8, 
            'servings': 2,
            'difficulty': 2},
        {
            'title': 'Full English',
            'description': 'Classic cooked breakfast',
            'ingredients': 'Sausages\nbacon\neggs\ntomato\nmushrooms',
            'instructions': 'Cook sausages\nbacon\ntomato and mushrooms in oven\nfry eggs in pan',
            'picture': 'recipes/full_english.jpg',
            'prep_time': 3,
            'cook_time': 20,
            'servings': 1,
            'difficulty': 1} ]
    
    lunch_recipes = [
        {
            'title': 'Chicken Wrap',
            'description': 'Wonderful chicken wrap to keep you going at work',
            'ingredients': 'Tortilla wrap\nchicken\nlettuce\ncheese',
            'instructions': 'Fry chicken\nadd chicken, lettuce, and cheese to tortilla\nwrap tighly',
            'picture': 'recipes/wrap.jpg',
            'prep_time': 1,
            'cook_time': 10,
            'servings': 1,
            'difficulty': 1 },
        {
            'title': 'Caesar Salad',
            'description': 'Delightful salad to enjoy a light lunch',
            'ingredients': 'Lettuce\ncroutons\nchicken\nbacon\ndressing',
            'instructions': 'Cook chicken and bacon\nadd ingredients to bowl\nmix',
            'picture': 'recipes/caesar_salad.jpg',
            'prep_time': 10,
            'cook_time': 10,
            'servings': 2,
            'difficulty': 1} ]
    
    dinner_recipes = [
        {
            'title': 'Margarita Pizza',
            'description': 'Cheese and mozzarella pizza for a quick easy dinner',
            'ingredients': 'dough\ntomato sauce\nmozzarella',
            'instructions': 'Spread sauce across dough\nsprinkle cheese on top\ncook in oven',
            'picture': 'recipes/pizza.avif',
            'prep_time': 5,
            'cook_time': 12,
            'servings': 2,
            'difficulty': 2 },
        {
            'title': 'Double Cheeseburger',
            'description': 'Delicious double cheeseburger for proper hearty meal',
            'ingredients': 'bun, burger patty\ntomato\nlettuce\ncheese',
            'instructions': 'Cook burger patty\nassemble burger', 
            'picture': 'recipes/double_cheeseburger.jpg',
            'prep_time': 5,
            'cook_time': 15,
            'servings': 1,
            'difficulty': 3} ]
    
    dessert_recipes = [
        {
            'title': 'Sticky Toffee Pudding',
            'description': 'Lovely sticky toffee pudding, perfect dessert',
            'ingredients': 'butter\nsugar\neggs\nflour\ntreacle\nmilk',
            'instructions': 'Combine butter\nsugar\neggs\nflour\nadd milk\nmelt butter in pan and add sugar and treacle for sauce\nbake pudding in oven\ncover with sauce', 
            'picture': 'recipes/sticky_toffee_pudding.jpg',
            'prep_time': 20,
            'cook_time': 40,
            'servings': 4,
            'difficulty': 3 },
        {
            'title': 'Banana Bread',
            'description': 'Quick and easy to make banana bread, great for using up overripe bananas for healhty-ish sweet treat',
            'ingredients': 'banana\nsugar\nbutter\nchocolate chips(optional)',
            'instructions': 'mash up bananas\ncombine banana mash with sugar and butter\nif using add chocolate chips\nbake in oven\nallow to cool',
            'picture': 'recipes/bananabread.jpg',
            'prep_time': 15,
            'cook_time': 30,
            'servings': 10,
            'difficulty': 1
        } ]
    
    snack_recipes = [
        {
            'title': 'Sliders',
            'description': 'Mini burgers, great as a snack between meals or when hosting',
            'ingredients': 'mini burger buns\nmini burgers\nlettuce\ntomato\nonion\ncheese',
            'instructions': 'Cook mini burgers in pan/oven\nplace cheese on a minute before cooked\ntoast buns\nassemble',
            'picture': 'recipes/sliders.jpg',
            'prep_time': 5,
            'cook_time': 15,
            'servings': 8,
            'difficulty': 2 },
        {
            'title': 'Cheese Toastie',
            'description': 'Nice comfort food, easy to make to get through till dinner/no time for proper lunch',
            'ingredients': 'bread\nbutter\ncheese\nany additional fillings',
            'instructions': 'butter bread\nadd cheese and any additional fillings\nform sandwich with buttered sides facing outwards\ntoast in machine',
            'picture': 'recipes/toastie.jpg',
            'prep_time': 8,
            'cook_time': 4,
            'servings': 1,
            'difficulty': 1 } ]
    
    drink_recipes = [
        {
            'title': 'Mojito',
            'description': 'Amazing cocktail, great for drinks with friends!!!',
            'ingredients': 'mint leaves\nlime juice\nrum\nsoda water\nice\nsugar',
            'instructions': 'muddle mint, lime juice and sugar\nadd rum\nadd ice and stir until sugar dissolved\ntop with soda water\ngarnish with mint leaves',
            'picture': 'recipes/mojito.jpg',
            'prep_time': 5,
            'cook_time': 0,
            'servings': 1,
            'difficulty': 1},
        {
            'title': 'Strawberry Daqiri',
            'description': 'Wonderful cocktail, great for pres or nice occasion - also amazing frozen',
            'ingredients': 'rum\nstrawberries\nlime juice\nsyrup\nice',
            'instructions': 'combine strawberries, rum, lime juice and syrup and blend\nshake with ice\nstrain',
            'picture': 'recipes/daq.jpg',
            'prep_time': 5,
            'cook_time': 0,
            'servings': 1,
            'difficulty': 1
        }  ]
    
    other_recipes = [
        {
            'title': 'Tomato Pasta Sauce',
            'description': 'Wonderful red tomato sauce, easy to make and great for pasta!',
            'ingredients': 'onion\ngarlic\ntomato passata\ntomato paste\noregano\nbasil\nsalt and pepper',
            'instructions': 'dice onion and cook off\nadd garlic and cook till fragrant\nadd passata, tomato paste, oregano, basil, salt and pepper\nsimmer',
            'picture': 'recipes/sauce.jpg',
            'prep_time': 8,
            'cook_time': 20,
            'servings': 2,
            'difficulty': 2
        }
    ]

    cats = {
        'Breakfast': breakfast_recipes,
        'Lunch': lunch_recipes,
        'Dinner': dinner_recipes,
        'Dessert': dessert_recipes,
        'Snack': snack_recipes,
        'Drink': drink_recipes,
        'Other': other_recipes
    }

    for cat_name, recipes in cats.items():
        cat = add_foodCategory(cat_name)
        for r in recipes:
            add_recipe(cat, r['title'], r['description'], r['ingredients'], r['instructions'], r['picture'], r['prep_time'], r['cook_time'], r['servings'], r['difficulty'])

    #Print results
    for c in FoodCategory.objects.all():
        print(f'Category: {c.name}')
        for r in Recipe.objects.filter(foodCategory=c):
            print(f'-Recipe: {r.title}')

def add_recipe(cat, title, description, ingredients, instructions, image_path=None, prep_time=None, cook_time=None, servings=None, difficulty=None):
    r = Recipe.objects.get_or_create(foodCategory=cat, title=title)[0]
    r.description = description
    r.ingredients = ingredients
    r.instructions = instructions
    r.prep_time=prep_time
    r.cook_time=cook_time
    r.servings=servings
    r.difficulty=difficulty
    if image_path:
        image_complete_path = os.path.join(settings.MEDIA_ROOT, image_path)
        with open(image_complete_path, 'rb') as f:
            r.picture.save(os.path.basename(image_complete_path), File(f), save=False)
    if not r.slug:
        r.slug = slugify(r.title)

    r.save()
    return r

def add_foodCategory(name):
    f = FoodCategory.objects.get_or_create(name=name)[0]
    return f

#execute
if __name__ == '__main__':
    print('Starting FlavourIndex population script...')
    populate()