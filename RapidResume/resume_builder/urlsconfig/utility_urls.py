from django.urls import path

from ..views import utitlity_views

urlpatterns = [
    path('generate_description_endpoint/<slug:form_slug>', utitlity_views.generate_description, name="get_auto_description"),
]

