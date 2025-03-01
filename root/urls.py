from django.urls import path,include
from . import views


app_name = "root"

urlpatterns = [
   path("",views.IndexView.as_view(),name='home'),
]