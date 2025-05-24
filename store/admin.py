from django.contrib import admin
from .models import Product,Variation

class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','price','stock','category','created_date']
    prepopulated_fields={'slug':('product_name',)}

admin.site.register(Product,ProductAdmin)

class variationAdmin(admin.ModelAdmin):
    list_display=['product','variation_value','variation_category','is_active']
    list_editable=['is_active']
    list_filter=['product','variation_value','variation_category','is_active']


admin.site.register(Variation,variationAdmin)
