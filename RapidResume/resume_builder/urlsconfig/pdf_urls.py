from django.urls import path

from ..views import pdf_views

app_name = 'pdfs'

urlpatterns = [
    path('download/unauth', pdf_views.download_resume_pdf, name='unauth_download'),
    path('download/auth/<int:resume_id>', pdf_views.download_resume_pdf, name='auth_download'),
]
