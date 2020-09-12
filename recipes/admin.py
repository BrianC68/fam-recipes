from django.contrib import admin
from . import models
from users.models import CustomUser


class RecipeAdmin(admin.ModelAdmin):

    list_display = ['title', 'contributor', 'published', 'date_published']
    search_fields = ['title', 'contributor']
    list_filter = ['contributor']
    prepopulated_fields = {'slug': ('title', )}


class IngredientListAdmin(admin.ModelAdmin):

    list_display = ['recipe', 'ingredient']
    search_fields = ['recipe']


class StepAdmin(admin.ModelAdmin):

    list_display = ['recipe', 'step_number', 'directions']


class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('category', )}


class CommentAdmin(admin.ModelAdmin):

    list_display = ['user', 'recipe', 'comment']


class CommentReplyAdmin(admin.ModelAdmin):

    list_display = ['user', 'comment', 'reply']


class FavoriteRecipeAdmin(admin.ModelAdmin):

    list_display = ['user', 'recipe']
    list_filter = ['user']


admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.IngredientList, IngredientListAdmin)
admin.site.register(models.Step, StepAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.CommentReply, CommentReplyAdmin)
admin.site.register(models.FavoriteRecipe, FavoriteRecipeAdmin)
