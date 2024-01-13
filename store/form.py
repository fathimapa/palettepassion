from django import forms
from .models import *

class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [ 'product_name', 'category', 'product_description', 'price', 'image']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = ['image']

