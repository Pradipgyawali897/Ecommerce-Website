from django.urls import path
from .views import create_view
urlpatterns = [
    path("create_product/",create_view,name="create_product"),
]
