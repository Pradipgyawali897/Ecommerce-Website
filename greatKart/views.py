from django.shortcuts import render 
from store.models import Product

def home(request):
    product=Product.objects.all().filter(is_avilable=True)
    return render(request,'home.html',context={"products":product})
