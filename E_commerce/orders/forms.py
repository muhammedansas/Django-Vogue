from django import forms
from .models import Order

class Orderform(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_first','address_second','country','state','city','order_note']

    def __init__(self,*args,**kwargs):
        super(Orderform,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'    