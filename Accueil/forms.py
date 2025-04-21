from django import forms
from .models import Category, Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ingrédients'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Instructions'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

 # Pour exclure certaines catégories lors de l'ajout
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(name__in=['Entrée', 'Dessert', 'Plats'])