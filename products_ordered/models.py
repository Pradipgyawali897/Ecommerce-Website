from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class product_ordered(models.Model):
    user=models.CharField(max_length=50)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    amount=models.IntegerField()
    