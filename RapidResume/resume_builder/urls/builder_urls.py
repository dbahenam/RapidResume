from django.urls import path

from ..views import builder_views

urlpatterns = [
    path("builder", builder_views.builder, name="builder"),
    path("new-resume", builder_views.new_resume, name="new_resume"),
    path("resume_preview", builder_views.resume_preview, name="resume_preview"),
    path("start-build", builder_views.start_resume_build, name="load_resume"),
]