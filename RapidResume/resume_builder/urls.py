from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("builder", views.builder, name="builder"),
    path("education", views.EducationView.as_view(), name="education"),
    path("work-experience", views.WorkExperienceView.as_view(), name="work-experience"),
    path("skill", views.SkillView.as_view(), name="skill"),
    path("certification", views.CertificationView.as_view(), name="certifications"),
    path("project", views.ProjectView.as_view(), name="project"),
    path("language", views.LanguageView.as_view(), name="language"),
    path("resume_preview", views.resume_preview, name="resume_preview")
]
