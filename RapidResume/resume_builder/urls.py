from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("builder", views.builder, name="builder"),
    path("personal_detail", views.PersonalDetailView.as_view(), name="perosnal_detail"),
    path("education", views.EducationView.as_view(), name="education"),
    path("work-experience", views.WorkExperienceView.as_view(), name="work-experience"),
    path("skill", views.SkillView.as_view(), name="skill"),
    path("certification", views.CertificationView.as_view(), name="certifications"),
    path("project", views.ProjectView.as_view(), name="project"),
    path("language", views.LanguageView.as_view(), name="language"),
    path("resume_preview", views.resume_preview, name="resume_preview"),
    path("start-build", views.start_resume_build, name="load_resume"),
    path("new-resume", views.new_resume, name="new_resume"),
    path('set_template/', views.set_template, name='set_template'),
    path('generate_description_endpoint/<slug:form_slug>', views.generate_description, name="get_auto_description"),
    path('download_resume/', views.download_resume_pdf, name='download_resume_pdf'),
]
