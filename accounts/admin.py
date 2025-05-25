from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import  UserAdmin


class Accountadmin(UserAdmin):
    list_display=['email','username','first_name','last_name','is_active'] # the uneditable field like ,'last_login','date_joined' cant be used it may cause a error from stack overflow As currently implemented, setting auto_now or auto_now_add to True will cause the field to have editable=False and blank=True set.

    filter_horizontal=()
    readonly_fields=['date_joined','last_login',]
    list_filter=('is_active',)
    ordering=['-date_joined']
admin.site.register(Account,Accountadmin)
