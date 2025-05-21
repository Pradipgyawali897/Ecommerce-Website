from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(blank=True,null=True)
    cat_image=models.ImageField(upload_to='photos/catogeries',blank=True)
    class Meta:
        verbose_name="categoty"
        verbose_name_plural="cateogries"
    def __str__(self):
        return self.name
    
