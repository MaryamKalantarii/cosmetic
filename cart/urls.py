from django.urls import path,include
from .views import *
from . import views

app_name='cart'


urlpatterns = [
    path("session/add-product/",views.SessionAddProductView.as_view(),name="session-add-product"),
    path("summary/",views.CartSummaryView.as_view(),name="cart-summary"),
    path("session/remove-product/",views.SessionRemoveProductView.as_view(),name="session-remove-product"),
    path("session/update-product-quantity/",views.SessionUpdateProductQuantityView.as_view(),name="session-update-product-quantity"),
    
]