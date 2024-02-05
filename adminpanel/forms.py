from django import forms
from django.forms import ClearableFileInput, inlineformset_factory
from store.models import *
from django.utils.text import slugify
from order.models import *
from banner_management.models import *
from django_countries.fields import CountryField
from bootstrap_datepicker_plus.widgets import DatePickerInput
import warnings
from PIL import Image

warnings.filterwarnings("ignore", category=FutureWarning)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.SlugField(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get('category_name')
        if category_name:
            cleaned_data['slug'] = slugify(category_name)
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widget = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        # Set the initial value for the slug field based on the product name
            product_name = self.initial.get('product_name')
            if product_name:
                self.initial['slug'] = slugify(product_name)

        def clean(self):
            price = self.cleaned_data['price']

            if price < 0:
                raise forms.ValidationError("Price cannot be negative.")

            image = self.cleaned_data.get('image')

            if image:
            # Check if the uploaded file is an image
                try:
                    with Image.open(image) as img:
                    # You can add more checks if needed, such as file size or image dimensions
                        if img.format.lower() not in ['jpeg', 'png', 'gif']:
                            raise forms.ValidationError(
                            "Only JPEG, PNG, or GIF images are allowed.")
                except Exception as e:
                    raise forms.ValidationError("Invalid image file.")


class ProductGalleryForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = '__all__'
        widgets = {
            'image': ClearableFileInput(attrs={'onchange': 'previewImage(this);'}),
        }


class VariationForm(forms.ModelForm):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extralarge', 'Extra Large'),

    ]
    size = forms.ChoiceField(choices=SIZE_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Variation
        fields = '__all__'
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        size = self.cleaned_data['size']
        product = self.cleaned_data['product']
        price = self.cleaned_data['price']

        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        

        # Check if a variation with the same size choice already exists for the product
        existing_variations = Variation.objects.filter(product=product, size=size)
        
        if self.instance and self.instance.pk:
            # Exclude the current instance when checking for existing variations during update
            existing_variations = existing_variations.exclude(pk=self.instance.pk)

        if existing_variations.exists():
            raise forms.ValidationError(f'A variation with size "{size}" already exists for this product.')


class OrderForm(forms.ModelForm):

    STATUS = [
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', "Shipped"),
        ('Out for delivery', "Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    ]
    status = forms.ChoiceField(
        choices=STATUS, widget=forms.Select(attrs={'class': 'form-control'}))
    
    

    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'order_note': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'order_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'is_ordered': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_returned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'return_reason': forms.TextInput(attrs={'class': 'form-control'}),
        }


ImageFormSet = inlineformset_factory(
    Product, ProductGallery, form=ProductGalleryForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'min_value', 'valid_to', 'active']

        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'valid_to': DatePickerInput(format='yyyy-mm-dd', attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'
        widgets = {
            'banner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'banner': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
