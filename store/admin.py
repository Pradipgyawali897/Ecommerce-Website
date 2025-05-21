from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price','stock','category','created_date']
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(Product,ProductAdmin)
