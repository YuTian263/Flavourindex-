from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class FoodCategory(models.Model):
    name = models.CharField(max_length=40, unique = True)

    def __str__(self):
        return self.name
    


class Recipe(models.Model):
    title = models.CharField(max_length=40, unique = False)
    description = models.TextField(max_length=200, unique = False)
    foodCategory = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    picture = models.ImageField(upload_to='recipes/', blank=True, null=True)
    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)
    difficulty = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'recipes'
        ordering = ['title']

    def __str__(self):
        return self.title

