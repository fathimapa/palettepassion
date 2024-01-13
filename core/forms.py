from django import forms
from  order.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line1','address_line2','country','state','city','zipcode']
    
    def __init__(self, *args, **kwargs):
      super(AddressForm,self).__init__(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
             