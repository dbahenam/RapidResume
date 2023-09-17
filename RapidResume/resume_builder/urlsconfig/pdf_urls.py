from django.urls import path

from ..views import pdf_views

urlpatterns = [
    path('download_resume/', pdf_views.download_resume_pdf, name='download_resume_pdf'),
]
