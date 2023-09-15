from django.urls import path

from ..views import user_views

urlpatterns = [
    path("user_profile", user_views.UserProfileView.as_view(), name="user_profile")
]
