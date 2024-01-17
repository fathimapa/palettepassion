from django import forms
from  order.models import Address
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line1', 'address_line2', 'country', 'state', 'city', 'zipcode']
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'custom-country-class form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'