"""portfolio_backend URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # Redirect root to API root
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('django-admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Serve media files (Django doesn't serve them by default in production with DEBUG=False)
    # Required for Render deployment since there is no S3 configured.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
