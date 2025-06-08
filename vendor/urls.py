from django.urls import path
from . import views

urlpatterns = [
    path('', views.retrive_view, name='vendor_dashboard'),
    path('create/', views.create_view, name='product_create'),
    path('update/<int:id>/', views.update_view, name='product_update'),
    path('delete/<int:id>/', views.delete_view, name='product_delete'),
    #path('products/remove-image/<int:product_id>/', views.remove_product_image, name='remove_product_image'),
    #path('products/', views.product_list, name='product_list'),
]