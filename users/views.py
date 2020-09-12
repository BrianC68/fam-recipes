from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from recipes.models import FavoriteRecipe


class SignUpView(CreateView):
    '''Page where users can sign up for an account.'''

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        # Assign slug by slugifying the username
        form.instance.slug = slugify(form.instance.username)
        return super().form_valid(form)


@login_required
def make_user_staff(request):
    '''This view makes the user a staff member so they can add and edit their recipes.'''

    user = CustomUser.objects.get(username=request.user.username)
    user.is_staff = True
    user.save()

    return redirect('recipes:recipes-index')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    '''Page where users can view their profile and other user profiles.'''

    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'custom_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the fav_recipes of the user who's profile is being viewed.
        context['fav_recipes'] = FavoriteRecipe.objects.filter(user=kwargs['object'].pk).order_by('recipe__title')
        return context
    


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''Page where users can update their profile information.'''

    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'user_change_form.html'

    def form_valid(self, form):
        # If the username has changed, change the slug
        form.instance.slug = slugify(form.instance.username)
        # Set the success url, takes user back to their profile page.
        self.success_url = reverse_lazy('users:profile', kwargs={ 'slug': form.instance.slug })
        return super().form_valid(form)
