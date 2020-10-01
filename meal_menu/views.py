from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView


from .models import MealMenuRecipe, ShoppingList, StoreDepartment
from .forms import UpdateShoppingListForm, CreateShoppingListForm
from recipes.models import Recipe, IngredientList, TryListRecipe


class MyMealMenuListView(LoginRequiredMixin, ListView):
    '''List of recipes on the weekly meal menu.'''

    model = MealMenuRecipe
    template_name = 'my-meal-menu-list.html'
    context_object_name = 'meal_menu'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('recipe__title')
        return queryset


@login_required
def add_to_meal_menu(request, slug, next):
    '''View that saves a recipe to users recipe meal menu.'''

    # Save the recipe to the users Meal Menu
    recipe = Recipe.objects.get(slug=slug)
    try:
        meal_menu_recipe = MealMenuRecipe(user=request.user, recipe=recipe)
        meal_menu_recipe.save()
        # Add message
        messages.add_message(request, messages.INFO, f'{recipe.title} has been added to your Meal Menu!')
    except IntegrityError:
        messages.add_message(request, messages.INFO, f'{recipe.title} is already on your Meal Menu')

    # Save the Recipes ingredient list to the users Shopping List
    ingredient_list = IngredientList.objects.filter(recipe=recipe)
    try:
        for ing in ingredient_list:
            shopping_list_item = ShoppingList.objects.create(user=request.user, recipe=recipe, list_item=ing.ingredient, department=ing.category)
        # Add message
        messages.add_message(request, messages.INFO, f'{recipe.title} ingredients have been added to your Shopping List')
    except IntegrityError:
        pass

    # If the recipe is on the Try List
    try:
        try_list_recipe = TryListRecipe.objects.get(recipe=recipe, user=request.user)
        try_list_recipe.delete()
    except ObjectDoesNotExist:
        pass

    # Return the success URL
    if next == 'my-recipes':
        return redirect('recipes:my-recipes')
    elif next == 'my-favorites':
        return redirect('recipes:my-favorites')
    elif next == 'my-try-list':
        return redirect('recipes:my-try-list')
    else:
        contributor = recipe.contributor
        return redirect('recipes:recipe-detail', slug=slug, contrib=contributor.slug)


@login_required
def remove_from_meal_menu(request, slug):
    '''View that removes a recipe from users recipe meal menu.'''

    # Remove the recipe from the users meal menu
    recipe = Recipe.objects.get(slug=slug)
    try:
        meal_menu_recipe = MealMenuRecipe.objects.get(recipe=recipe, user=request.user)
        meal_menu_recipe.delete()
        # Add message
        messages.add_message(request, messages.INFO, f'{recipe.title} has been removed from your Meal Menu')
    except ObjectDoesNotExist:
        messages.add_message(request, messages.INFO, f'{recipe.title} was not on your Meal Menu')

    try:
        shopping_list_items = ShoppingList.objects.filter(recipe=recipe)
        if shopping_list_items:
            messages.add_message(request, messages.INFO, f'{recipe.title} ingredients were removed from your Shopping List')
            shopping_list_items.delete()
    except ObjectDoesNotExist:
        pass

    # Return the success URL
    contributor = recipe.contributor
    return redirect('meal_menu:my-meal-menu')


class ShoppingListView(LoginRequiredMixin, ListView):
    '''Shopping List of ingredients from Meal Menu recipes. \\
    Users are able to add additional items to the shopping list.'''

    model = ShoppingList
    template_name = 'my-shopping-list.html'
    context_object_name = 'shopping_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('department')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = ShoppingList.objects.order_by('department').values('department__id', 'department__store_department').distinct()
        return context


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    '''View that allows users to add items to their shopping list.'''

    model = ShoppingList
    form_class = CreateShoppingListForm
    template_name = 'shopping-list-item-add.html'
    success_url = reverse_lazy('meal_menu:my-shopping-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.recipe = None
        # Add Message
        messages.add_message(self.request, messages.INFO, f'{form.instance.list_item} has been added to your Shopping List')
        return super().form_valid(form)


class ShoppingListUpdateView(LoginRequiredMixin, UpdateView):
    '''View that allows users to change a shopping list item.'''

    model = ShoppingList
    form_class = UpdateShoppingListForm
    template_name = 'shopping-list-item-edit.html'

    def form_valid(self, form):
        # Get current value of list item being changed.
        item = self.model.objects.get(pk=self.kwargs['pk']).list_item
        dept = self.model.objects.get(pk=self.kwargs['pk']).department

        # Add Message
        if item != form.instance.list_item and dept != form.instance.department:
            msg = f'{item} has been changed to {form.instance.list_item} and department has been changed to {form.instance.department}'
        elif item != form.instance.list_item:
            msg= f'{item} has been changed to {form.instance.list_item}'
        elif dept != form.instance.department:
            msg = f'Department for {item} has been changed from {dept} to {form.instance.department}'

        messages.add_message(self.request, messages.INFO, msg)

        self.success_url = reverse_lazy('meal_menu:my-shopping-list')
        return super().form_valid(form)


@login_required
def remove_from_shopping_list(request, item_pk):
    '''View that removes an item from the shopping list.'''

    # Get the item to be removed and delete it if it exists.
    try:
        list_item = ShoppingList.objects.get(pk=item_pk)
        # Add Message
        messages.add_message(request, messages.INFO, f'{list_item.list_item} has been removed from your Shopping List!')
        list_item.delete()
    except ObjectDoesNotExist:
        pass

    return redirect('meal_menu:my-shopping-list')
