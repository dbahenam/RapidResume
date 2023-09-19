from django.urls import path, include
from ..views.form_views import unauth_form_views

app_name = 'unauth'

urlpatterns = [
    # Unauthenticated paths
    path("personal_detail", unauth_form_views.PersonalDetailView.as_view(), name="personal_detail"),
    path("education", unauth_form_views.EducationView.as_view(), name="education"),
    path("work_experience", unauth_form_views.WorkExperienceView.as_view(), name="work_experience"),
    path("skill", unauth_form_views.SkillView.as_view(), name="skill"),
    path("certification", unauth_form_views.CertificationView.as_view(), name="certification"),
    path("project", unauth_form_views.ProjectView.as_view(), name="project"),
    path("language", unauth_form_views.LanguageView.as_view(), name="language"),
]
