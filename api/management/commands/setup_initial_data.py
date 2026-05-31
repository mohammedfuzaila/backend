"""
Management command: setup_initial_data
Runs during build on Render to:
  1. Create Django superuser (if not exists)
  2. Create singleton model instances (Hero, About, SiteSettings, SeoSettings)

Safe to run multiple times — uses get_or_create everywhere.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create initial superuser and singleton data for production deployment'

    def handle(self, *args, **options):
        User = get_user_model()

        # ── 1. Create superuser ──────────────────────────────────────────
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email    = os.getenv('DJANGO_SUPERUSER_EMAIL', 'anaikarmohammedfuzail57@gmail.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin@fuzail2025')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️  Superuser "{username}" already exists — skipping'))

        # ── 2. Create singleton model instances ──────────────────────────
        from api.models import HeroSection, AboutSection, SiteSettings, SeoSettings

        hero, created = HeroSection.objects.get_or_create(id=1)
        self.stdout.write(self.style.SUCCESS('✅ HeroSection ready') if created else '⚠️  HeroSection already exists')

        about, created = AboutSection.objects.get_or_create(id=1)
        self.stdout.write(self.style.SUCCESS('✅ AboutSection ready') if created else '⚠️  AboutSection already exists')

        settings_obj, created = SiteSettings.objects.get_or_create(id=1)
        self.stdout.write(self.style.SUCCESS('✅ SiteSettings ready') if created else '⚠️  SiteSettings already exists')

        seo, created = SeoSettings.objects.get_or_create(id=1)
        self.stdout.write(self.style.SUCCESS('✅ SeoSettings ready') if created else '⚠️  SeoSettings already exists')

        self.stdout.write(self.style.SUCCESS('\n🚀 Initial data setup complete!'))
