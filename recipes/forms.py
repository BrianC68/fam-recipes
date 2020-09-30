from django import forms

from recipes.models import Recipe, IngredientList, Step, Comment, CommentReply


class CreateRecipeForm(forms.ModelForm):
    '''Form used to add a recipe to the Recipe model.'''

    class Meta:
        model = Recipe
        exclude = ['slug', 'contributor', 'published', 'date_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = ('Title')
        self.fields['description'].widget.attrs['placeholder'] = ('Description')
        self.fields['prep_time'].widget.attrs['placeholder'] = ('Prep Time')
        self.fields['cook_time'].widget.attrs['placeholder'] = ('Cook Time')
        self.fields['servings'].widget.attrs['placeholder'] = ('Servings')
        self.fields['special_notes'].widget.attrs['placeholder'] = ('Notes')


class CreateIngredientListForm(forms.ModelForm):
    '''Form used to add ingredients to the ingredient list model.'''

    class Meta:
        model = IngredientList
        fields = ['recipe', 'ingredient', 'category']
        widgets = {
            'recipe': forms.HiddenInput()
        }


class CreateStepForm(forms.ModelForm):
    '''Form used to add directions to the recipe model.'''

    class Meta:
        model = Step
        fields = ['recipe', 'step_number', 'directions']
        widgets = {
            'recipe': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['step_number'].widget.attrs['placeholder'] = ('Step Number')
        self.fields['directions'].widget.attrs['placeholder'] = ('Directions')


class UpdateRecipeForm(forms.ModelForm):
    '''Form used to update recipe information.'''

    class Meta:
        model = Recipe
        exclude = ['contributor', 'published', 'date_published']
        widgets = {
            'slug': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = ('Title')
        self.fields['description'].widget.attrs['placeholder'] = ('Description')
        self.fields['prep_time'].widget.attrs['placeholder'] = ('Prep Time')
        self.fields['cook_time'].widget.attrs['placeholder'] = ('Cook Time')
        self.fields['servings'].widget.attrs['placeholder'] = ('Servings')
        self.fields['special_notes'].widget.attrs['placeholder'] = ('Notes')


class UpdateIngredientForm(forms.ModelForm):
    '''Form used to update an ingredient.'''

    class Meta:
        model = IngredientList
        fields = ['recipe', 'ingredient', 'category']
        widgets = {
            'recipe': forms.HiddenInput()
        }


class UpdateStepForm(forms.ModelForm):
    '''Form used to update a direction.'''

    class Meta:
        model = Step
        fields = ['recipe', 'step_number', 'directions']
        widgets = {
            'recipe': forms.HiddenInput()
        }


class CreateCommentForm(forms.ModelForm):
    '''Form used to add a comment to a recipe.'''

    class Meta:
        model = Comment
        fields = ['recipe', 'user', 'comment']
        widgets = {
            'recipe': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }


class CreateCommentReplyForm(forms.ModelForm):
    '''Form used to add a reply to a recipe comment.'''

    class Meta:
        model = CommentReply
        fields = ['comment', 'user', 'reply']
        widgets = {
            'comment': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
