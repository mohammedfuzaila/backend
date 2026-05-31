"""portfolio_backend URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redirect root to API root
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('django-admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
