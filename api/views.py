from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    HeroSection, AboutSection, Skill, Project, Experience,
    Certificate, Testimonial, BlogPost, ContactMessage,
    SocialLink, SeoSettings, SiteSettings, Service
)
from .serializers import (
    HeroSectionSerializer, AboutSectionSerializer, SkillSerializer,
    ProjectSerializer, ExperienceSerializer, CertificateSerializer,
    TestimonialSerializer, BlogPostSerializer, ContactMessageSerializer,
    SocialLinkSerializer, SeoSettingsSerializer, SiteSettingsSerializer,
    ServiceSerializer, DashboardStatsSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# ─── Public Read-Only ViewSets ───────────────────────────────────────────────

class HeroSectionView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        hero = HeroSection.objects.filter(is_active=True).first()
        if not hero:
            return Response({})
        serializer = HeroSectionSerializer(hero, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        hero = HeroSection.objects.first()
        if not hero:
            hero = HeroSection.objects.create()
        serializer = HeroSectionSerializer(hero, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class AboutSectionView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        about = AboutSection.objects.filter(is_active=True).first()
        if not about:
            return Response({})
        serializer = AboutSectionSerializer(about, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        about = AboutSection.objects.first()
        if not about:
            about = AboutSection.objects.create()
        serializer = AboutSectionSerializer(about, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_active']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Skill.objects.all()
        return Skill.objects.filter(is_active=True)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_featured', 'is_active']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(is_active=True)

    def get_serializer_context(self):
        return {'request': self.request}


class ExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ExperienceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'is_active']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Experience.objects.all()
        return Experience.objects.filter(is_active=True)


class CertificateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Certificate.objects.all()
        return Certificate.objects.filter(is_active=True)

    def get_serializer_context(self):
        return {'request': self.request}


class TestimonialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(is_active=True)

    def get_serializer_context(self):
        return {'request': self.request}


class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_published', 'category']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(is_published=True)

    def get_serializer_context(self):
        return {'request': self.request}


class ContactMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ContactMessageSerializer

    def get_queryset(self):
        return ContactMessage.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg = serializer.save()

        # Send email notification via Brevo SMTP
        try:
            from django.core.mail import EmailMessage

            email_body = (
                f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                f'  NEW CONTACT FORM MESSAGE\n'
                f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                f'Name:    {msg.name}\n'
                f'Email:   {msg.email}\n'
                f'Subject: {msg.subject}\n\n'
                f'──────────── Message ────────────\n\n'
                f'{msg.message}\n\n'
                f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
                f'Reply directly to this email to respond to {msg.name}\n'
            )

            email = EmailMessage(
                subject=f'Portfolio Contact: {msg.subject} — from {msg.name}',
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.RECIPIENT_EMAIL],
                reply_to=[msg.email],
            )
            email.send(fail_silently=True)
        except Exception:
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SocialLinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return SocialLink.objects.all()
        return SocialLink.objects.filter(is_active=True)


class SeoSettingsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        seo = SeoSettings.objects.first()
        if not seo:
            return Response({})
        serializer = SeoSettingsSerializer(seo, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        seo = SeoSettings.objects.first()
        if not seo:
            seo = SeoSettings.objects.create()
        serializer = SeoSettingsSerializer(seo, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SiteSettingsView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        s = SiteSettings.objects.first()
        if not s:
            return Response({})
        serializer = SiteSettingsSerializer(s)
        return Response(serializer.data)

    def patch(self, request):
        s = SiteSettings.objects.first()
        if not s:
            s = SiteSettings.objects.create()
        serializer = SiteSettingsSerializer(s, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ServiceSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Service.objects.all()
        return Service.objects.filter(is_active=True)


# ─── Admin Dashboard Stats ────────────────────────────────────────────────────

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
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


@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def mark_message_read(request, pk):
    try:
        msg = ContactMessage.objects.get(pk=pk)
        msg.is_read = True
        msg.save()
        return Response({'status': 'marked as read'})
    except ContactMessage.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
