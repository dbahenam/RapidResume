from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("builder", views.builder, name="builder"),
    path("education", views.education, name="education"),
    path("work-experience", views.work_experience, name="work-experience"),
    path("skills", views.skills, name="skills"),
    path("certifications", views.certifications, name="certifications"),
]
