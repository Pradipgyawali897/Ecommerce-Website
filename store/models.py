
from django.db import models
from category.models import Category
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
import random

from django.core.exceptions import ObjectDoesNotExist
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products',null=True,blank=True)
    stock = models.IntegerField()
    is_avilable = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

        
    def save(self, *args, **kwargs):
        # Generate slug only for new instances
        if not self.pk and not self.slug:
            base_slug = slugify(self.product_name)
            slug = base_slug
            counter = 1
            while True:
                try:
                    Product.objects.get(slug=slug)
                    # Append a counter instead of random number for simpler uniqueness
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                except ObjectDoesNotExist:
                    self.slug = slug
                    break
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_view', args=[self.category.slug, self.slug])


# Choices for variation category
variation_category_choice = (
    ('colour', 'Colour'),
    ('size', 'Size'),
)


# Custom Manager


# Variation Model
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.variation_value
