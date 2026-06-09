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
    
    # Serve media files from the database (solves Render ephemeral storage issue)
    path('api/media/<path:name>', getattr(__import__('api.views', fromlist=['serve_media']), 'serve_media')),
]
