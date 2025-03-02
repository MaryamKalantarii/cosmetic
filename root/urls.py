from django.urls import path,include
from django.urls import path,include
from . import views

app_name='root'

urlpatterns = [
   path("",views.IndexView.as_view(),name='home'),
   path("about",views.AboutView.as_view(),name='about'),
   path("contact",views.ContactView.as_view(),name='contact'),
   path("submit/ticket/", views.SendContactView.as_view(), name="submit-ticket"),
   path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),

]