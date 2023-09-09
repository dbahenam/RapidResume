from django.urls import path

from ..views import form_views

urlpatterns = [
    path("personal_detail", form_views.PersonalDetailView.as_view(), name="perosnal_detail"),
    path("education", form_views.EducationView.as_view(), name="education"),
    path("work-experience", form_views.WorkExperienceView.as_view(), name="work-experience"),
    path("skill", form_views.SkillView.as_view(), name="skill"),
    path("certification", form_views.CertificationView.as_view(), name="certifications"),
    path("project", form_views.ProjectView.as_view(), name="project"),
    path("language", form_views.LanguageView.as_view(), name="language"),
    path('generate_description_endpoint/<slug:form_slug>', form_views.generate_description, name="get_auto_description"),
]