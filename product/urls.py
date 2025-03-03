from django.urls import path,include,re_path
from .views import *
from . import views

app_name='product'


urlpatterns = [
    path('grid/',ProductGridView.as_view(),name="product-grid"),
    re_path(r"(?P<slug>[-\w]+)/detail/",views.ProductDetailView.as_view(),name="product-detail"),
    path("add-or-remove-wishlist/",views.AddOrRemoveWishlistView.as_view(),name="add-or-remove-wishlist"),
   
]