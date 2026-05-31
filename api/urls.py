from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    HeroSectionView, AboutSectionView, SkillViewSet, ProjectViewSet,
    ExperienceViewSet, CertificateViewSet, TestimonialViewSet,
    BlogPostViewSet, ContactMessageViewSet, SocialLinkViewSet,
    SeoSettingsView, SiteSettingsView, ServiceViewSet,
    DashboardStatsView, mark_message_read
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'blogs', BlogPostViewSet, basename='blog')
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'social-links', SocialLinkViewSet, basename='social-link')
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    # JWT Auth
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Singleton sections
    path('hero/', HeroSectionView.as_view(), name='hero'),
    path('about/', AboutSectionView.as_view(), name='about'),
    path('seo/', SeoSettingsView.as_view(), name='seo'),
    path('settings/', SiteSettingsView.as_view(), name='settings'),

    # Admin
    path('admin/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('admin/messages/<int:pk>/read/', mark_message_read, name='mark-read'),

    # ViewSets
    path('', include(router.urls)),
]
