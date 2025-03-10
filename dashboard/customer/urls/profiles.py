from django.urls import path
from .. import views

urlpatterns = [
    path("home/", views.CustomerDashboardHomeView.as_view(), name="home"),
    path("security/edit/",views.CustomerSecurityEditView.as_view(),name="security-edit"),
    path("profile/edit/",views.CustomerProfileEditView.as_view(),name="profile-edit"),
    path("profile/image/edit/",views.CustomerProfileImageEditView.as_view(),name="profile-image-edit"),
]
