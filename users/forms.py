from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'UserName'
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['email'].label = 'Email Address'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'birthplace', 'picture', 'slug']
        widgets = {
            'slug': forms.HiddenInput(),
        }
