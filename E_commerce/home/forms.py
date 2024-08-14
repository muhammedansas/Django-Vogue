from django import forms
from django.core.validators import EmailValidator

class Contact_form(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',  # Add your CSS class here
                'placeholder': 'Enter your name'  # Add placeholder here
            }
        )
    )          
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',  # Add your CSS class here
                'placeholder': 'Enter your email'  # Add placeholder here
            }
        )
    )
    subject = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Add your CSS class here
                'placeholder': 'Enter the subject'  # Add placeholder here
            }
        )
    )