from django.contrib import admin
from . import models
from users.models import CustomUser


class MealMenuRecipeAdmin(admin.ModelAdmin):

    list_display = ['user', 'recipe']
    list_filter = ['user']


class ShoppingListAdmin(admin.ModelAdmin):

    list_display = ['user', 'list_item', 'recipe']
    list_filter = ['user']


class StoreDepartmentAdmin(admin.ModelAdmin):

    pass


admin.site.register(models.MealMenuRecipe, MealMenuRecipeAdmin)
admin.site.register(models.ShoppingList, ShoppingListAdmin)
admin.site.register(models.StoreDepartment, StoreDepartmentAdmin)
