from django import forms

from meal_menu.models import ShoppingList, StoreDepartment


class CreateShoppingListForm(forms.ModelForm):
    '''Form used to add an item to the shopping list.'''

    class Meta:
        model = ShoppingList
        fields = ['list_item', 'department']


class UpdateShoppingListForm(forms.ModelForm):
    '''Form used to update a shopping list item.'''

    class Meta:
        model = ShoppingList
        fields = ['list_item', 'department']
