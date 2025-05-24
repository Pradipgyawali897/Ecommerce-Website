from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name="store"),
    path('category/<slug:categoty_slug>/',views.store,name="products_by_category"),
    path('category/<slug:categoty_slug>/<slug:product_slug>/',views.product_detail,name="product_view"),
    path('search/',views.search_view,name="search"),
]
