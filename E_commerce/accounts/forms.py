from django import forms
from . models import Account,Userprofile
import re
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError,FieldError

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
    }), validators=[
        MinLengthValidator(8, "Password must be at least 8 characters long.")
    ])
    phone_number = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits long."
            )
        ],
        widget=forms.TextInput(attrs={
            "class": "form-control",
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password does not match")

        # Ensure that the password is valid
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.") 
            
        
class Userform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number') 

    def __init__(self,*args,**kwargs):
        super(Userform,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'     

class Userprofileform(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages={'invalid':("Images files only")},widget=forms.FileInput)
    class Meta:
        model = Userprofile
        fields = ('user','address_first','address_second','profile_picture','city','state','country') 

    def __init__(self,*args,**kwargs):
        super(Userprofileform,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'    
