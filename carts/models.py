from django.db import models
from store.models import Product,Variation

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cart_id
    
class CartIteam(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField(blank=True,null=True)
    is_active=models.BooleanField(default=True)
    def __unicode__(self):
        return self.product
    
    def get_total(self):
        return self.quantity*self.product.price