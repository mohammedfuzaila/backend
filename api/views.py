"""
Django views for the portfolio API.

All endpoints return identical responses to the frontend.
OperationalError / ProgrammingError guards prevent HTTP 500 when the
database has not been migrated yet (e.g. fresh SQLite on cold-start).
"""

import logging
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import OperationalError, ProgrammingError, connection

logger = logging.getLogger(__name__)

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    AboutSection, BlogPost, Certificate, ContactMessage, Experience,
    HeroSection, Project, SeoSettings, Service, SiteSettings, Skill,
    SocialLink, Testimonial,
)
from .serializers import (
    AboutSectionSerializer, BlogPostSerializer, CertificateSerializer,
    ContactMessageSerializer, DashboardStatsSerializer, ExperienceSerializer,
    HeroSectionSerializer, ProjectSerializer, SeoSettingsSerializer,
    ServiceSerializer, SiteSettingsSerializer, SkillSerializer,
    SocialLinkSerializer, TestimonialSerializer,
)


# ---------------------------------------------------------------------------
# Custom permission
# ---------------------------------------------------------------------------

class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow safe (read-only) methods to everyone; write access only to staff."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# ---------------------------------------------------------------------------
# Singleton section views (Hero, About, Seo, SiteSettings)
# ---------------------------------------------------------------------------

class HeroSectionView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            hero = HeroSection.objects.filter(is_active=True).first()
            if not hero:
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = HeroSectionSerializer(hero, context={'request': request})
            return Response(serializer.data)
        except (OperationalError, ProgrammingError):
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        try:
            hero = HeroSection.objects.first()
            if not hero:
                hero = HeroSection.objects.create()
            serializer = HeroSectionSerializer(
                hero, data=request.data, partial=True, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (OperationalError, ProgrammingError) as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class AboutSectionView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            about = AboutSection.objects.filter(is_active=True).first()
            if not about:
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = AboutSectionSerializer(about, context={'request': request})
            return Response(serializer.data)
        except (OperationalError, ProgrammingError):
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        try:
            about = AboutSection.objects.first()
            if not about:
                about = AboutSection.objects.create()
            serializer = AboutSectionSerializer(
                about, data=request.data, partial=True, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (OperationalError, ProgrammingError) as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class SeoSettingsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            seo = SeoSettings.objects.first()
            if not seo:
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = SeoSettingsSerializer(seo, context={'request': request})
            return Response(serializer.data)
        except (OperationalError, ProgrammingError):
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        try:
            seo = SeoSettings.objects.first()
            if not seo:
                seo = SeoSettings.objects.create()
            serializer = SeoSettingsSerializer(
                seo, data=request.data, partial=True, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (OperationalError, ProgrammingError) as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class SiteSettingsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            s = SiteSettings.objects.first()
            if not s:
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = SiteSettingsSerializer(s)
            return Response(serializer.data)
        except (OperationalError, ProgrammingError):
            return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        try:
            s = SiteSettings.objects.first()
            if not s:
                s = SiteSettings.objects.create()
            serializer = SiteSettingsSerializer(s, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (OperationalError, ProgrammingError) as e:
            return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# ---------------------------------------------------------------------------
# ViewSets (list/detail endpoints via DefaultRouter)
# ---------------------------------------------------------------------------

class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_active']

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return Skill.objects.all()
            return Skill.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return Skill.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_featured', 'is_active']

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return Project.objects.all()
            return Project.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return Project.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])




class ExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'is_active']

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return Experience.objects.all()
            return Experience.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return Experience.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])


class CertificateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return Certificate.objects.all()
            return Certificate.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return Certificate.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])




class TestimonialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return Testimonial.objects.all()
            return Testimonial.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return Testimonial.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])




class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_published', 'category']

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return BlogPost.objects.all()
            return BlogPost.objects.filter(is_published=True)
        except (OperationalError, ProgrammingError):
            return BlogPost.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])




class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        try:
            return ContactMessage.objects.all()
        except (OperationalError, ProgrammingError):
            return ContactMessage.objects.none()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            msg = serializer.save()

            # Send email notification — fail_silently so a mail error never
            # prevents the contact message from being saved.
            try:
                email_body = (
                    f'New contact form message\n\n'
                    f'Name:    {msg.name}\n'
                    f'Email:   {msg.email}\n'
                    f'Subject: {msg.subject}\n\n'
                    f'Message:\n{msg.message}\n\n'
                    f'Reply directly to this email to respond to {msg.name}.'
                )
                email = EmailMessage(
                    subject=f'Portfolio Contact: {msg.subject} - from {msg.name}',
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.RECIPIENT_EMAIL],
                    reply_to=[msg.email],
                )
                email.send(fail_silently=False)
            except Exception as e:
                logger.error(f"Error sending contact email notification: {e}", exc_info=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (OperationalError, ProgrammingError):
            return Response(
                {'error': 'Database not ready. Please try again later.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class SocialLinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return SocialLink.objects.all()
            return SocialLink.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return SocialLink.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])


class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                return Service.objects.all()
            return Service.objects.filter(is_active=True)
        except (OperationalError, ProgrammingError):
            return Service.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except (OperationalError, ProgrammingError):
            return Response([])


# ---------------------------------------------------------------------------
# Admin-only views
# ---------------------------------------------------------------------------

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        try:
            data = {
                'total_projects': Project.objects.count(),
                'total_skills': Skill.objects.count(),
                'total_messages': ContactMessage.objects.count(),
                'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
                'total_blogs': BlogPost.objects.count(),
                'published_blogs': BlogPost.objects.filter(is_published=True).count(),
                'total_testimonials': Testimonial.objects.count(),
                'total_certificates': Certificate.objects.count(),
            }
            return Response(data)
        except (OperationalError, ProgrammingError):
            return Response({
                'total_projects': 0,
                'total_skills': 0,
                'total_messages': 0,
                'unread_messages': 0,
                'total_blogs': 0,
                'published_blogs': 0,
                'total_testimonials': 0,
                'total_certificates': 0,
            })


@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def mark_message_read(request, pk):
    try:
        msg = ContactMessage.objects.get(pk=pk)
        msg.is_read = True
        msg.save()
        return Response({'status': 'marked as read'})
    except ContactMessage.DoesNotExist:
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    except (OperationalError, ProgrammingError) as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


# ---------------------------------------------------------------------------
# Health check (public)
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """
    Public diagnostic endpoint.
    Returns DB engine, whether DATABASE_URL is set, and migration status.
    """
    result = {'status': 'ok', 'database': 'unknown', 'error': None}

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        result['database'] = 'connected'

        tables = connection.introspection.table_names()
        result['tables_found'] = len(tables)
        result['has_hero_table'] = 'api_herosection' in tables
        result['db_engine'] = connection.settings_dict.get('ENGINE', 'unknown')
        result['database_url_set'] = bool(os.getenv('DATABASE_URL'))
        result['migration_needed'] = not result['has_hero_table']

    except Exception as e:
        result['status'] = 'error'
        result['database'] = 'failed'
        result['error'] = str(e)

    return Response(result)

from django.http import HttpResponse, Http404
from urllib.parse import unquote
from api.models import MediaFile

def serve_media(request, name):
    name = unquote(name)
    try:
        f = MediaFile.objects.get(name=name)
        return HttpResponse(f.content, content_type=f.content_type)
    except MediaFile.DoesNotExist:
        raise Http404('Media file not found')