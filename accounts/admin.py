from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


class Accountadmin(UserAdmin):
    list_display=['email','username','first_name','last_name','is_active','last_login','date_joined']
    filter_horizontal=()
    list_filter=()
    ordering=['-date_joined']
admin.site.register(Account,Accountadmin)
