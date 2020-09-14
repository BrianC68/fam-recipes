from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils.text import slugify

from PIL import Image

from users.models import CustomUser
from fam_recipes.settings import MEDIA_ROOT

import os

def get_upload_path(instance, filename):
        return os.path.join(f'{instance.contributor.last_name.lower()}-{instance.contributor.first_name.lower()}/{slugify(instance.title)}/', filename)


class Recipe(models.Model):
    '''The recipe class.'''

    # Model fields
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(help_text='A short paragraph or two that describes the recipe, including from whom or where you got it.')
    contributor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    picture = models.ImageField(upload_to=get_upload_path, blank=True, null=True, help_text='Please use landscape photos.')
    prep_time = models.IntegerField(null=False, blank=False, help_text='Enter time in minutes.')
    cook_time = models.IntegerField(null=True, blank=True, help_text='Enter time in minutes.')
    servings = models.IntegerField(null=True, blank=True)
    special_notes = models.TextField(blank=True, null=True, help_text='Modifcations, options, etc.')
    categories = models.ManyToManyField('Category', related_name='recipes', help_text='Hold Ctrl + Click to enter multiple categories.')
    published = models.BooleanField(default=False)
    date_published = models.DateField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=False)

    class Meta:
        unique_together = ['title', 'contributor']
        ordering = ['-date_published']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:sharing', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save()
        max_size = (920, 920)
        try:
            img = Image.open(self.picture.path)
            if img.height > 920 or img.width > 920:
                img.thumbnail(max_size, Image.ANTIALIAS)
                img.save(self.picture.path, "JPEG")
        except:
            pass
        return super().save(*args, **kwargs)


class IngredientList(models.Model):
    '''Model holds the list of ingredients for a recipe.'''

    # Model fields
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.CharField(max_length=255)

    class Meta:
        unique_together = ['recipe', 'ingredient']
        ordering = ['pk']
        verbose_name_plural = 'Indredient Lists'

    def __str__(self):
        return f'Ingredient for {self.recipe}'

    def get_absolute_url(self):
        return reverse('recipes:add-ingredients', kwargs={'pk': self.recipe.id})


class Step(models.Model):
    '''Model holds the preparation steps for a recipe.'''

    # Model fields
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    directions = models.TextField(help_text='Describe what to do in this step.')
    verbose_name = 'Direction'

    class Meta:
        unique_together = ['recipe', 'step_number']
        ordering = ['step_number']

    def __str__(self):
        return self.verbose_name


    def get_absolute_url(self):
        return reverse('recipes:add-directions', kwargs={'pk': self.recipe.id})


class Category(models.Model):
    '''Model holds different recipe categories.  Many to many relationship with Recipe Class.'''

    # Model Fields
    category = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['category']

    def __str__(self):
        return self.category


class Comment(models.Model):
    '''Model that stores comments related to recipes.'''

    # Model fields
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'For: {self.recipe.title}'


class CommentReply(models.Model):
    '''Model that stores replies to recipe comments.  Only the contributor can reply to their own recipe comments.'''

    # Model Fields
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reply = models.TextField()

    class Meta:
        verbose_name_plural = 'Comment Replies'
        ordering = ['pk']


class FavoriteRecipe(models.Model):
    '''Model that stores users favorite recipes.'''

    # Model Fields
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorite_recipes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Favorite Recipes'
