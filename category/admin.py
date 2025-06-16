from django.contrib import admin

from .models import Category,Vendor_Pannel_Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']
admin.site.register(Category,CategoryAdmin)

class Vendor_Pannel_Category_Manager(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']
admin.site.register(Vendor_Pannel_Category,Vendor_Pannel_Category_Manager)