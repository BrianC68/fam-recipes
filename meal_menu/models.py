from django.db import models

from users.models import CustomUser
from recipes.models import IngredientList, Recipe


class MealMenuRecipe(models.Model):
    '''Model that stores recipes the user has on their weekly meal menu.'''

    # Model Fields
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='menu_recipes')

    class Meta:
        verbose_name_plural = 'Meal Menu Recipes'
        unique_together = ['recipe', 'user']


class StoreDepartment(models.Model):
    '''Model holds grocery store department choices used for organizing the shopping list.'''

    # Model Fields
    store_department = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Store Departments'
        ordering = ['store_department']

    def __str__(self):
        return self.store_department


class ShoppingList(models.Model):
    '''Model that holds shopping list items.  Ingredients from MealMenu recipes 
        are added to the shopping list when placed on the meal menu.'''

    # Model Fields
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    list_item = models.CharField(max_length=255)
    department = models.ForeignKey(
        StoreDepartment, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text = 'Used to group shopping list items. (Not Required)'
        )

    class Meta:
        verbose_name_plural = 'Shopping Lists'
        unique_together = ['user', 'list_item', 'recipe']

    def __str__(self):
        return self.list_item
