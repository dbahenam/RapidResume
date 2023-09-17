from django.urls import path

from ..views import builder_views

app_name = 'resume_builder'

urlpatterns = [
    path("dashboard", builder_views.resume_dashboard, name="resume_dashboard"),
    path("create", builder_views.create_new_resume, name="create_new_resume"),
    path("preview", builder_views.preview_resume, name="preview_resume"),
]