from django.urls import path

from . import views


app_name = 'meal_menu'

urlpatterns = [
    path('add/<slug>/', views.add_to_meal_menu, name='add-to-meal-menu'),
    path('add/<slug>/<next>/', views.add_to_meal_menu, name='add-to-meal-menu'),
    path('remove/<slug>/', views.remove_from_meal_menu, name='remove-from-meal-menu'),
    path('my-meals/', views.MyMealMenuListView.as_view(), name='my-meal-menu'),
    path('shopping-list/', views.ShoppingListView.as_view(), name='my-shopping-list'),
    path('shopping-list/remove/<item_pk>/', views.remove_from_shopping_list, name='my-shopping-list-remove'),
    path('shopping-list/update/<pk>', views.ShoppingListUpdateView.as_view(), name='shopping-list-item-edit'),
    path('shopping-list/add/', views.ShoppingListCreateView.as_view(), name='shopping-list-item-add'),

]
