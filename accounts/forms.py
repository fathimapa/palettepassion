from typing import Any
from django import forms
from .models import *
from phonenumbers.phonenumberutil import NumberParseException
import re




class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password'
    }))
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder' : 'confirm Password'
    }))

    class Meta:
        model  = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args,**kwargs):
        super(RegisterationForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegisterationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
        phone_number = cleaned_data.get('phone_number')
        import phonenumbers

        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number")
        
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        # Custom validation for first_name and last_name
        if not re.match(r'^[a-zA-Z ]+$', first_name):
            raise forms.ValidationError(
                "First name can only contain letters and spaces!"
            )
           

        if not re.match(r'^[a-zA-Z ]+$', last_name):
            raise forms.ValidationError(
                "Last name can only contain letters and spaces!"
            )
        
        
    
        
        
    def __init__(self, *args , ** kwargs):
        super(RegisterationForm , self).__init__(*args , ** kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class EditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email']

    def __init__(self,*args,**kwargs):
        super(EditForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput) 
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'