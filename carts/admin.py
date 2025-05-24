from django.contrib import admin
from .models import Cart,CartIteam

class CartAdmin(admin.ModelAdmin):
    list_display=['cart_id','date']
admin.site.register(Cart,CartAdmin)
class CartIteamAdmin(admin.ModelAdmin):
    list_display=['product','cart','quantity','is_active']
    list_editable=['is_active']
admin.site.register(CartIteam,CartIteamAdmin)