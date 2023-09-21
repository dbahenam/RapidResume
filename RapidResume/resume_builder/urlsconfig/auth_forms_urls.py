from django.urls import path, include
from ..views.form_views import auth_form_views

app_name = 'auth'

urlpatterns = [
    # Authenticated paths
    path("personal_detail/<int:resume_id>", auth_form_views.PersonalDetailView.as_view(), name="personal_detail"),
    path("education/<int:resume_id>", auth_form_views.EducationView.as_view(), name="education"),
    path("work-experience/<int:resume_id>", auth_form_views.WorkExperienceView.as_view(), name="work_experience"),
    path("skill/<int:resume_id>", auth_form_views.SkillView.as_view(), name="skill"),
    path("certification/<int:resume_id>", auth_form_views.CertificationView.as_view(), name="certification"),
    path("project/<int:resume_id>", auth_form_views.ProjectView.as_view(), name="project"),
    path("language/<int:resume_id>", auth_form_views.LanguageView.as_view(), name="language"),
]
