from django.urls import path
from . import views

urlpatterns = [
    path('',views.cart,name="cart"),
    path('add-cart/<int:product_id>',views.add_cart,name="add_cart"),
    path('remove-cart/<int:product_id>/<int:cart_iteam_id>',views.remove_cart,name="remove_cart"),
    path('remove-all-cartiteam/<int:product_id>/<int:cart_iteam_id>',views.remove_cart_iteam,name="remove_cart_iteams"),

]
