from django.forms import ModelForm
from store.models import Product
from django import forms

class MyProductForm(ModelForm):
    class Meta:
        model=Product
        fields=['product_name','product_description','price','images','stock','category']
        

    