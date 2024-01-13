from django import forms
from django.utils.text import slugify
from .models import category  # Replace 'Category' with your model name

class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ['category_name', 'description', 'category_image']

    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get('category_name')
        if category_name:
            cleaned_data['slug'] = slugify(category_name)
        return cleaned_data
