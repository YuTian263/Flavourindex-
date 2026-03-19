import warnings
from django.test import TestCase
import os
import re

from flavourindexApp.models import FoodCategory, Recipe
from populate_flavourindex import populate
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Population_Script_Tests(TestCase):
    
    def setUp(self):
        populate()

    def test_population_script_creates_recipes_and_categories(self):
        self.assertTrue(Recipe.objects.count() > 0, f"{FAILURE_HEADER}Population script does not create recipes{FAILURE_FOOTER}")
        self.assertTrue(FoodCategory.objects.count() > 0, f"{FAILURE_HEADER}Population script does not create categories{FAILURE_FOOTER}")



class gitignore_Tests(TestCase):
    
    def does_gitignore_include_database(self, path):
        f = open(path, 'r')
        for line in f:
            line = line.strip()
            if line.startswith('db.sqlite3'):
                return True
        f.close()
        return False
    
    def test_gitignore_for_database(self):      
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        gitignore_path = os.path.join(git_base_dir, '.gitignore')
        if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}Your .gitignore file does not include 'db.sqlite3'{FAILURE_FOOTER}")
        else:
            warnings.warn("No gitignore file in repository")



class ViewsTests(TestCase):

    def setUp(self):
        category = FoodCategory.objects.create(name="Test Category")
        self.recipe = Recipe.objects.create(title="Test Recipe", description="Short description", foodCategory=category, ingredients="Test ingredients", instructions="Test instructions")

    def login(self):
        user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

    def test_add_recipe_view(self):
        self.login()
        response = self.client.get(reverse('flavourindexApp:add_recipe'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Add Recipe doesn't load{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'add_recipe.html', f"{FAILURE_HEADER}Add Recipe doesn't use add recipe template{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'base.html', f"{FAILURE_HEADER}Add Recipe doesn't use base template{FAILURE_FOOTER}")

    def test_index_view(self):
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Index doesn't load{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'index.html', f"{FAILURE_HEADER}Index doesn't use index template{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'base.html', f"{FAILURE_HEADER}Index doesn't use base template{FAILURE_FOOTER}")

    def test_login_view(self):
        response = self.client.get(reverse('flavourindexApp:login'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Login doesn't load{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'login.html', f"{FAILURE_HEADER}Login doesn't use login template{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'base.html', f"{FAILURE_HEADER}Login doesn't use base template{FAILURE_FOOTER}")

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('flavourindexApp:recipe_detail', args =[self.recipe.id]))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Recipe detail doesn't load{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'recipe_detail.html', f"{FAILURE_HEADER}Recipe detail doesn't use recipe_detail template{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'base.html', f"{FAILURE_HEADER}Recipe detial doesn't use base template{FAILURE_FOOTER}")

    def test_register_core_tests(self):
        response = self.client.get(reverse('flavourindexApp:register'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Register doesn't load{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'register.html', f"{FAILURE_HEADER}Register doesn't use login template{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'base.html', f"{FAILURE_HEADER} doesn't use base template{FAILURE_FOOTER}")



class Model_Tests(TestCase):
     
    def test_food_category_creation(self):
        category = FoodCategory.objects.create(name="Dinner")
        self.assertEqual(category.name, "Dinner", f"{FAILURE_HEADER}Food category could not be succesfully created{FAILURE_FOOTER}")

    def test_recipe_creation(self):
        category = FoodCategory.objects.create(name="Dinner")
        recipe = Recipe.objects.create(title="Pizza", description="Tasty pizza", foodCategory=category, ingredients="dough, cheese, sauce", instructions="Cook for 12 mins")
        self.assertEqual(recipe.title, "Pizza", f"{FAILURE_HEADER}Recipe could not be succesfully created{FAILURE_FOOTER}")
        self.assertEqual(recipe.description, "Tasty pizza", f"{FAILURE_HEADER}Recipe could not be succesfully created{FAILURE_FOOTER}")
        self.assertEqual(recipe.foodCategory, category, f"{FAILURE_HEADER}Recipe could not be succesfully created{FAILURE_FOOTER}")
        self.assertEqual(recipe.ingredients, "dough, cheese, sauce", f"{FAILURE_HEADER}Recipe could not be succesfully created{FAILURE_FOOTER}")
        self.assertEqual(recipe.instructions, "Cook for 12 mins", f"{FAILURE_HEADER}Recipe could not be succesfully created{FAILURE_FOOTER}")

    def test_food_category_str(self):
        category = FoodCategory.objects.create(name="Dinner")
        self.assertEqual("Dinner", str(category), f"{FAILURE_HEADER}Category __str__ method doesn't work")

    def test_recipe_category_str(self):
        category = FoodCategory.objects.create(name="Dinner")
        recipe = Recipe.objects.create(title="Pizza", description="Tasty pizza", foodCategory=category, ingredients="dough, cheese, sauce", instructions="Cook for 12 mins")
        self.assertEqual("Pizza", str(recipe), f"{FAILURE_HEADER}Recipe __str__ method doesn't work")

    def test_recipe_slug(self):
        category = FoodCategory.objects.create(name="Dinner")
        recipe = Recipe.objects.create(title="Margarita Pizza", description="Tasty pizza", foodCategory=category, ingredients="dough, cheese, sauce", instructions="Cook for 12 mins")
        self.assertEqual("margarita-pizza", recipe.slug, f"{FAILURE_HEADER}Recipe slug not working correctly{FAILURE_FOOTER}")



class AddRecipeTests(TestCase):

    def setUp(self):
        category = FoodCategory.objects.create(name="Test Category")
        self.recipe = Recipe.objects.create(title="Test Recipe", description="Short description", foodCategory=category, ingredients="Test ingredients", instructions="Test instructions")

    def login(self):
        user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")
    
    def test_add_recipe_must_be_logged_in(self):
        response = self.client.get(reverse('flavourindexApp:add_recipe'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}User authentication not working{FAILURE_FOOTER}")

    def test_add_recipe_contains_form(self):
        self.login()
        response = self.client.get(reverse('flavourindexApp:add_recipe'))
        self.assertContains(response, '<form', count=None, msg_prefix=f"{FAILURE_HEADER}Add recipe template doesn't contain form{FAILURE_FOOTER}")
        self.assertContains(response, 'method="POST"', count=None, msg_prefix= f"{FAILURE_HEADER}Add recipe template form isn't post{FAILURE_FOOTER}")
    
    def test_add_recipe_page_text_exists(self):
        self.login()
        response = self.client.get(reverse('flavourindexApp:add_recipe'))
        self.assertContains(response, 'Add a Recipe', count=None, msg_prefix= f"{FAILURE_HEADER}Add recipe page text not displaying{FAILURE_FOOTER}")
        self.assertContains(response, 'Share something tasty', count=None, msg_prefix= f"{FAILURE_HEADER}Add recipe page text not displaying{FAILURE_FOOTER}")



class BaseTests(TestCase):

    def test_base_core_tests(self):
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Base doesn't load{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'base.html', f"{FAILURE_HEADER}Base doesn't use base template{FAILURE_FOOTER}")

    def test_blocks_exist(self):
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertContains(response, '<title>FlavourIndex - Home</title>', count=None, msg_prefix=f"{FAILURE_HEADER}Title Block not working{FAILURE_FOOTER}")
        self.assertContains(response, '<h2>All Recipes</h2>', count=None, msg_prefix=f"{FAILURE_HEADER}Body Block not working{FAILURE_FOOTER}")

    def test_navbar_logged_in(self):
        user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertContains(response, 'Add Recipe', count=None, msg_prefix=f"{FAILURE_HEADER}Navbar logged in doesn't have add recipe{FAILURE_FOOTER}")
        self.assertContains(response, 'Logout', count=None, msg_prefix=f"{FAILURE_HEADER}Navbar doesn't have logout when logged in{FAILURE_FOOTER}")

    def test_navbar_logged_out(self):
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertContains(response, 'Recipes', count=None, msg_prefix=f"{FAILURE_HEADER}Navbar logged out doesn't have recipes{FAILURE_FOOTER}")
        self.assertContains(response, 'Login', count=None, msg_prefix=f"{FAILURE_HEADER}Navbar logged out doesn't have login{FAILURE_FOOTER}")
        self.assertContains(response, 'Register', count=None, msg_prefix=f"{FAILURE_HEADER}Navbar logged out doesn't have register{FAILURE_FOOTER}")
        self.assertNotContains(response, 'Add Recipe', msg_prefix="{FAILURE_HEADER}Navbar logged out has login needed links{FAILURE_FOOTER}")
        self.assertNotContains(response, 'Logout', msg_prefix="{FAILURE_HEADER}Navbar logged out has login needed links{FAILURE_FOOTER}")



class IndexTests(TestCase):

    def test_index_content(self):
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertContains(response, 'h2>All Recipes</h2>', count=None, msg_prefix= f"{FAILURE_HEADER}Index doesn't contain all content{FAILURE_FOOTER}")
        self.assertContains(response, 'Explore your new food haven!', count=None, msg_prefix=f"{FAILURE_HEADER}Index doesn't contain all content{FAILURE_FOOTER}")

    def test_search_form(self):
        response = self.client.get(reverse('flavourindexApp:index'))
        self.assertContains(response, '<form', count=None, msg_prefix=f"{FAILURE_HEADER}Error with search form{FAILURE_FOOTER}")
        self.assertContains(response, 'method="GET"', count=None, msg_prefix=f"{FAILURE_HEADER}Search form isn't of GET{FAILURE_FOOTER}")
        self.assertContains(response, 'type="submit"', count=None, msg_prefix=f"{FAILURE_HEADER}Search form of wrong type{FAILURE_FOOTER}")



class LoginTests(TestCase):

    def test_login_form_exists(self):
        response = self.client.get(reverse('flavourindexApp:login'))
        self.assertContains(response, '<form', count=None, msg_prefix=f"{FAILURE_HEADER}Login doesn't contain form{FAILURE_FOOTER}")
        self.assertContains(response, 'method="post"', count=None, msg_prefix=f"{FAILURE_HEADER}Form type isn't post{FAILURE_FOOTER}")

    def test_input_fields_exist(self):
        response = self.client.get(reverse('flavourindexApp:login'))
        self.assertContains(response, 'name="username"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't have username input field{FAILURE_FOOTER}")
        self.assertContains(response, 'name="password"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't contain password field{FAILURE_FOOTER}")

    def test_register_link(self):
        response = self.client.get(reverse('flavourindexApp:login'))
        self.assertContains(response, reverse('flavourindexApp:register'))



class RecipeDetailTests(TestCase):

    def setUp(self):
        category = FoodCategory.objects.create(name="Test Category")
        self.recipe = Recipe.objects.create(title="Test Recipe", description="Short description", foodCategory=category, ingredients="Test ingredients", instructions="Test instructions")

    def test_recipe_core_fields(self):
        response = self.client.get(reverse('flavourindexApp:recipe_detail', args =[self.recipe.id]))
        self.assertContains(response, self.recipe.title, count=None, msg_prefix= f"{FAILURE_HEADER}Recipe doesn't display title")
        self.assertContains(response, self.recipe.description, count=None, msg_prefix= f"{FAILURE_HEADER}Recipe doesn't display description{FAILURE_FOOTER}")
        self.assertContains(response, self.recipe.ingredients, count=None, msg_prefix= f"{FAILURE_HEADER}Recipe doesn't display ingredients{FAILURE_FOOTER}")
        self.assertContains(response, self.recipe.instructions, count=None, msg_prefix= f"{FAILURE_HEADER}Recipe doesn't display instructions{FAILURE_FOOTER}")

    def test_recipe_image(self):
        self.recipe.picture = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        self.recipe.save()
        response = self.client.get(reverse('flavourindexApp:recipe_detail', args=[self.recipe.id]))
        self.assertContains(response, self.recipe.picture.url)



class RegisterTests(TestCase):

    def test_login_form_exists(self):
        response = self.client.get(reverse('flavourindexApp:register'))
        self.assertContains(response, '<form', count=None, msg_prefix=f"{FAILURE_HEADER}Register doesn't contain form{FAILURE_FOOTER}")
        self.assertContains(response, 'method="post"', count=None, msg_prefix=f"{FAILURE_HEADER}Form type isn't post{FAILURE_FOOTER}")

    def test_input_fields_exist(self):
        response = self.client.get(reverse('flavourindexApp:register'))
        self.assertContains(response, 'name="username"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't have username input field{FAILURE_FOOTER}")
        self.assertContains(response, 'name="email"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't contain email field{FAILURE_FOOTER}")
        self.assertContains(response, 'name="first_name"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't have first name input field{FAILURE_FOOTER}")
        self.assertContains(response, 'name="last_name"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't have last name input field{FAILURE_FOOTER}")
        self.assertContains(response, 'name="password1"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't have password input field{FAILURE_FOOTER}")
        self.assertContains(response, 'name="password2"', count=None, msg_prefix=f"{FAILURE_HEADER}Form doesn't have confirm password input field{FAILURE_FOOTER}")

    def test_register_link(self):
        response = self.client.get(reverse('flavourindexApp:register'))
        self.assertContains(response, reverse('flavourindexApp:login'))
