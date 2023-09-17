from django.urls import path, include

urlpatterns = [
    path('', include('resume_builder.urlsconfig.home_urls')),
    path('resume_builder/', include('resume_builder.urlsconfig.builder_urls')),
    path('unauth/', include('resume_builder.urlsconfig.unauth_forms_urls')),
    path('auth/', include('resume_builder.urlsconfig.auth_forms_urls')),
]