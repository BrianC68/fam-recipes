from django.views.generic import ListView, CreateView, UpdateView, \
    DetailView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.mail import send_mass_mail, send_mail
from django.db.models import ObjectDoesNotExist
from django.db import IntegrityError

from datetime import date

from .models import Recipe, IngredientList, Step, Category, Comment, CommentReply, \
    FavoriteRecipe, TryListRecipe
from .forms import CreateRecipeForm, CreateIngredientListForm, CreateStepForm, \
    UpdateRecipeForm, UpdateIngredientForm, UpdateStepForm, CreateCommentForm, \
    CreateCommentReplyForm
from users.models import CustomUser
from meal_menu.models import MealMenuRecipe, ShoppingList


class RecipeListView(LoginRequiredMixin, ListView):
    '''Page that displays the list of recipes.'''

    model = Recipe
    template_name = 'recipes_index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class RecipeDetailView(LoginRequiredMixin, DetailView):
    '''Page that displays the recipe detail.'''

    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            FavoriteRecipe.objects.get(recipe__slug=self.kwargs['slug'], user=self.request.user)
            context['is_favorite'] = True
        except ObjectDoesNotExist:
            context['is_favorite'] = False

        try:
            TryListRecipe.objects.get(recipe__slug=self.kwargs['slug'], user=self.request.user)
            context['on_try_list'] = True
        except ObjectDoesNotExist:
            context['on_try_list'] = False


        try:
            MealMenuRecipe.objects.get(recipe__slug=self.kwargs['slug'], user=self.request.user)
            context['on_meal_menu'] = True
        except ObjectDoesNotExist:
            context['on_meal_menu'] = False

        return context


class RecipeShareView(LoginRequiredMixin, TemplateView):
    '''Page where steps to add a recipe are displayed.'''

    template_name = 'share_recipe_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in kwargs.keys():
            context['recipe'] = Recipe.objects.get(pk=kwargs['pk'])
            context['num_ings'] = IngredientList.objects.filter(recipe=kwargs['pk']).count()
            context['num_dirs'] = Step.objects.filter(recipe=kwargs['pk']).count()
            context['unpublished_recipes'] = Recipe.objects.filter(contributor=self.request.user, published=False).exclude(pk=kwargs['pk'])
        else:
            context['unpublished_recipes'] = Recipe.objects.filter(contributor=self.request.user, published=False)
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    '''Page where user can add a recipe.'''

    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'recipe_add.html'

    def form_valid(self, form):
        # Assign user as contributor
        form.instance.contributor = self.request.user
        # Create slug field from recipe title
        form.instance.slug = slugify(form.instance.title)
        # Save the object
        self.object = form.save(commit=False)
        # Set the message
        messages.add_message(self.request, messages.SUCCESS, 'Your recipe information has been saved!')

        return super().form_valid(form)


class IngredientListCreateView(LoginRequiredMixin, CreateView):
    '''Page where user can add ingredients to the ingredient list for a particular recipe.'''

    model = IngredientList
    form_class = CreateIngredientListForm
    template_name = 'ingredient_list_add.html'

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial['recipe'] = self.kwargs['pk']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = Recipe.objects.get(pk=self.kwargs['pk'])
        context['ing_list'] = self.model.objects.filter(recipe=self.kwargs['pk'])
        return context


class StepCreateView(LoginRequiredMixin, CreateView):
    '''Page where user can add directions for a particular recipe.'''

    model = Step
    form_class = CreateStepForm
    template_name = 'directions_step_add.html'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial['recipe'] = self.kwargs['pk']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = Recipe.objects.get(pk=self.kwargs['pk'])
        context['steps'] = self.model.objects.filter(recipe=self.kwargs['pk'])
        return context


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    '''Page where user can update recipe information.'''

    model = Recipe
    form_class = UpdateRecipeForm
    template_name = 'recipe_edit.html'

    def form_valid(self, form):
        # Slugify the recipe title
        form.instance.slug = slugify(form.instance.title)

        # Add Message
        messages.add_message(self.request, messages.INFO, f'{form.instance.title} has been updated!')
        return super().form_valid(form)


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    '''Page where user can update an ingredient.'''

    model = IngredientList
    form_class = UpdateIngredientForm
    template_name = 'ingredient_edit.html'
    # success_url = reverse_lazy('recipes:recipes-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_pk'] = self.model.objects.get(pk=self.kwargs['pk']).recipe.pk
        return context

    def form_valid(self, form):
        # Set the success URL based on what recipe is being shared
        self.success_url = reverse_lazy('recipes:add-ingredients', kwargs={'pk': form.instance.recipe.pk})
        messages.add_message(self.request, messages.SUCCESS, 'Your ingredient has been updated!')
        return super().form_valid(form)


class StepUpdateView(LoginRequiredMixin, UpdateView):
    '''Page where user can update an ingredient.'''

    model = Step
    form_class = UpdateStepForm
    template_name = 'directions_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_pk'] = self.model.objects.get(pk=self.kwargs['pk']).recipe.pk
        return context

    def form_valid(self, form):

        # Set the success URL based on what recipe is being shared
        self.success_url = reverse_lazy('recipes:add-directions', kwargs={ 'pk': form.instance.recipe.pk })

        # Add Message
        messages.add_message(self.request, messages.SUCCESS, f'Direction number {form.instance.step_number} has been updated!')
        
        return super().form_valid(form)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    '''View deletes an ingredient from the recipe.'''
    
    model = IngredientList

    def delete(self, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, 'Your ingredient has been removed!')
        self.success_url = reverse_lazy('recipes:add-ingredients', kwargs={ 'pk': kwargs['recipe'] })

        return super().delete(*args, **kwargs)


class StepDeleteView(LoginRequiredMixin, DeleteView):
    '''View deletes a direction from the recipe.'''

    model = Step

    def delete(self, *args, **kwargs):

        # Get the direction object being deleted
        direction = Step.objects.get(pk=kwargs['pk'])
        
        # Add Message
        messages.add_message(self.request, messages.INFO, f'Direction number {direction.step_number} has been removed!')
        # Set the success url
        self.success_url = reverse_lazy('recipes:add-directions', kwargs={ 'pk': kwargs['recipe'] })

        return super().delete(*args, **kwargs)


@login_required
def publish_recipe(request, pk):
    '''This view publishes the recipe by setting published=True and date_published=datetime.date.today().'''

    recipe = Recipe.objects.all().get(id=pk) # Get recipe object
    recipe.published = True # Set publish to True
    recipe.date_published = date.today() # Set date_published to today's date
    recipe.save() # Save the object
    # Set success message.
    messages.add_message(request, messages.SUCCESS, 'Your recipe is now live on the website! Thank you for sharing with the family!')

    # Email all users that a new recipe has been added
    recipients = CustomUser.objects.filter(is_active=True).exclude(username=request.user.username).values_list('email', flat=True)
    from_email = 'noreply@famrecipes.net'
    subject = 'New Recipe on FamRecipes.net'
    message = f'{request.user.get_full_name()} has added a recipe to FamRecipes.net, {recipe.title}.\n\n'
    message += f'See it here: https://www.famrecipes.net/recipes/detail/{request.user.slug}/{recipe.slug}/\n\n'
    message += 'FamRecipes.net'
    new_recipe_email = (subject, message, from_email, recipients)

    try:
        send_mass_mail((new_recipe_email, ))
    except:
        pass

    return redirect('recipes:sharing', pk=recipe.id)


class BrowseListView(LoginRequiredMixin, ListView):
    '''Page where users can browse recipes by category or contributor.'''

    model = Category
    user_model = CustomUser
    context_object_name = 'categories'
    template_name = 'browse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contributors'] = self.user_model.objects.filter(is_staff=True).order_by('last_name')
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    '''Page that lists all the recipes in a given category.'''

    model = Recipe
    template_name = 'category_list_view.html'
    context_object_name = 'recipes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(slug=self.kwargs['slug']).values_list('category', flat=True)[0]
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(categories__slug__in=[self.kwargs['slug'], ]).order_by('title')
        return queryset


class ContributorListView(LoginRequiredMixin, ListView):
    '''Page that lists all the recipes added by a given contributor.'''

    model = Recipe
    template_name = 'contributor_list_view.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contributor'] = CustomUser.objects.get(username=self.kwargs['contrib'])
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(contributor__username=self.kwargs['contrib']).order_by('title')
        return queryset


class CommentCreateView(LoginRequiredMixin, CreateView):
    '''Page where users can add comments to a recipe.'''

    model = Comment
    template_name = 'comment_add_form.html'
    form_class = CreateCommentForm

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()
        initial['recipe'] = Recipe.objects.get(slug=self.kwargs['slug']).id
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_name'] = Recipe.objects.get(slug=self.kwargs['slug']).title
        return context

    def form_valid(self, form):
        # Set the success url
        self.success_url = reverse_lazy('recipes:recipe-detail', kwargs={ 'slug': self.kwargs['slug'], 'contrib': form.instance.recipe.contributor.slug })

        # Send email to recipe contributor that someone commented on the recipe
        to_email = form.instance.recipe.contributor.email
        from_email = 'noreply@famrecipes.net'
        subject = 'You got a comment!'
        message = f'{form.instance.user.get_full_name()} commented on your {form.instance.recipe.title} recipe.\n\n'
        message += f'View it here: https://www.famrecipes.net/recipes/detail/{form.instance.recipe.contributor.slug}/{form.instance.recipe.slug}/\n\n'
        message += 'FamRecipes.net'

        try:
            send_mail(subject, message, from_email, [to_email])
        except:
            pass

        return super().form_valid(form)


class CommentReplyCreateView(LoginRequiredMixin, CreateView):
    '''Page where users can reply to comments made about their recipes.'''

    model = CommentReply
    template_name = 'comment_reply_add_form.html'
    form_class = CreateCommentReplyForm

    def get_initial(self):
        initial = super().get_initial()
        initial['comment'] = Comment.objects.get(pk=self.kwargs['pk'])
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = Comment.objects.get(pk=self.kwargs['pk']).comment
        return context

    def form_valid(self, form):
       
        # Set the success URL
        self.success_url = reverse_lazy('recipes:recipe-detail', kwargs={ 'slug': form.instance.comment.recipe.slug, 'contrib': form.instance.comment.recipe.contributor.slug })

        # Send email to commentor that someone replied to their comment
        to_email = form.instance.comment.user.email
        from_email = 'noreply@famrecipes.net'
        subject = 'You got a reply!'
        message = f'{form.instance.user.get_full_name()} replied to your comment on the {form.instance.comment.recipe.title} recipe.\n\n'
        message += f'View it here: https://www.famrecipes.net/recipes/detail/{form.instance.comment.recipe.contributor.slug}/{form.instance.comment.recipe.slug}/\n\n'
        message += 'FamRecipes.net'

        try:
            send_mail(subject, message, from_email, [to_email])
        except:
            pass

        return super().form_valid(form)


@login_required
def add_to_favorites(request, slug):
    '''View that saves a recipe to users favorite recipes list.'''

    recipe = Recipe.objects.get(slug=slug)
    favorite = FavoriteRecipe(user=request.user, recipe=recipe)
    favorite.save()

    # Add message
    messages.add_message(request, messages.INFO, 'Added to your Favorites')

    # Return the success URL
    contributor = recipe.contributor
    return redirect('recipes:recipe-detail', slug=slug, contrib=contributor.slug)


@login_required
def remove_from_favorites(request, slug):
    '''View that removes a recipe from users favorite recipes list.'''

    recipe = Recipe.objects.get(slug=slug)
    favorite = FavoriteRecipe.objects.get(recipe=recipe, user=request.user)
    favorite.delete()

    # Add message
    messages.add_message(request, messages.INFO, f'{recipe.title} was removed from your Favorites')
    
    # Return the success URL
    contributor = recipe.contributor
    return redirect('recipes:my-favorites')


@login_required
def add_to_try_list(request, slug):
    '''View that saves a recipe to users recipe try list.'''

    recipe = Recipe.objects.get(slug=slug)
    try_list_recipe = TryListRecipe(user=request.user, recipe=recipe)
    try_list_recipe.save()

    # Add message
    messages.add_message(request, messages.INFO, 'Added to your Try List')

    # Return the success URL
    contributor = recipe.contributor
    return redirect('recipes:recipe-detail', slug=slug, contrib=contributor.slug)


@login_required
def remove_from_try_list(request, slug):
    '''View that removes a recipe from users recipe try list.'''

    recipe = Recipe.objects.get(slug=slug)
    try_list_recipe = TryListRecipe.objects.get(recipe=recipe, user=request.user)
    try_list_recipe.delete()

    # Return the success URL
    contributor = recipe.contributor
    return redirect('recipes:my-try-list')


@login_required
def move_from_try_list_to_meal_menu(request, slug):
    '''View that moves a recipe from the Try List to the Meal Menu and adds ingredients to the Shopping List'''

    recipe = Recipe.objects.get(slug=slug)
    # Add the recipe to the Meal Menu
    try:
        meal_menu_recipe = MealMenuRecipe(user=request.user, recipe=recipe)
        meal_menu_recipe.save()
    except IntegrityError:
        messages.add_message(request, messages.INFO, 'This recipe is already on your Meal Menu! You may remove it from your Try List.')

    # Save the Recipes ingredient list to the users Shopping List
    ingredient_list = IngredientList.objects.filter(recipe=recipe)
    for ing in ingredient_list:
        try:
            shopping_list_item = ShoppingList.objects.create(user=request.user, recipe=recipe, list_item=ing.ingredient, department=ing.category)
        except IntegrityError:
            pass

    # Remove the recipe from the Try List
    try:
        try_list_recipe = TryListRecipe.objects.get(recipe=recipe, user=request.user)
        try_list_recipe.delete()
    except ObjectDoesNotExist:
        pass

    # Add message
    messages.add_message(request, messages.INFO, f'{recipe.title} has been moved to your Meal Menu and all ingredients have been added to your shopping list')
    # Return the success URL
    contributor = recipe.contributor
    return redirect('recipes:my-try-list')


class MyTryListView(LoginRequiredMixin, ListView):
    '''List of recipes the user would like to try.'''

    model = TryListRecipe
    template_name = 'my_try_list.html'
    context_object_name = 'try_list_recipes'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('recipe__title')
        return queryset


class MyFavoritesListView(LoginRequiredMixin, ListView):
    '''List of recipes the user has saved to favorites.'''

    model = FavoriteRecipe
    template_name = 'my-fav-list.html'
    context_object_name = 'fav_recipes'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('recipe__title')
        return queryset


class MyRecipesListView(LoginRequiredMixin, ListView):
    '''List of recipes the user has contributed.'''

    model = Recipe
    template_name = 'my-recipes-list.html'
    context_object_name = 'my_recipes'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(contributor=self.request.user).order_by('title')
        return queryset
