from django.urls import path

from ..views import pdf_views

urlpatterns = [
    path("new-resume", pdf_views.new_resume, name="new_resume"),
    path('set_template/', pdf_views.set_template, name='set_template'),
    path('download_resume/', pdf_views.download_resume_pdf, name='download_resume_pdf'),
]
