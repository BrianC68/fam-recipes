from django.urls import path

from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipes-index'),
    path('share/', views.RecipeShareView.as_view(), name='share'),
    path('share/add/', views.RecipeCreateView.as_view(), name='add-recipe-info'),
    path('share/<pk>/', views.RecipeShareView.as_view(), name='sharing'),
    path('detail/<contrib>/<slug>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('share/add/ingredients/<pk>/', views.IngredientListCreateView.as_view(), name='add-ingredients'),
    path('share/add/directions/<pk>/', views.StepCreateView.as_view(), name='add-directions'),
    path('share/edit/recipe/<slug>', views.RecipeUpdateView.as_view(), name='edit-recipe-info'),
    path('share/edit/ingredient/<pk>/', views.IngredientUpdateView.as_view(), name='edit-ingredient'),
    path('share/edit/direction/<pk>/', views.StepUpdateView.as_view(), name='edit-direction'),
    path('share/delete/ingredient/<pk>/<recipe>/', views.IngredientDeleteView.as_view(), name='delete-ingredient'),
    path('share/delete/direction/<pk>/<recipe>/', views.StepDeleteView.as_view(), name='delete-direction'),
    path('share/publish/<pk>/', views.publish_recipe, name='publish-recipe'),
    path('browse/', views.BrowseListView.as_view(), name='browse'),
    path('browse/<slug>/', views.CategoryListView.as_view(), name='browse-categories'),
    path('browse/user/<contrib>/', views.ContributorListView.as_view(), name='browse-contributor'),
    path('comment/add/<slug>/', views.CommentCreateView.as_view(), name='add-comment'),
    path('comment/reply/<pk>', views.CommentReplyCreateView.as_view(), name='add-comment-reply'),
    path('favorites/add/<slug>/', views.add_to_favorites, name='add-to-favs'),
    path('favorites/remove/<slug>/', views.remove_from_favorites, name='remove-from-favs'),

]