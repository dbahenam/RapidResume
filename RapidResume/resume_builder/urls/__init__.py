# urls/__init__.py
from .home_urls import urlpatterns as home_patterns
from .form_urls import urlpatterns as form_patterns
from .builder_urls import urlpatterns as builder_patterns
from .pdf_urls import urlpatterns as pdf_patterns
from .user_urls import urlpatterns as user_patterns

urlpatterns = home_patterns + form_patterns + builder_patterns + pdf_patterns + user_patterns