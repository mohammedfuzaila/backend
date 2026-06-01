"""
Management command: setup_initial_data

Runs during build on Render to:
  1. Create Django superuser (if not exists)
  2. Create singleton model instances (Hero, About, SiteSettings, SeoSettings)

Safe to run multiple times — uses get_or_create everywhere.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create initial superuser and singleton data for production deployment'

    def handle(self, *args, **options):
        User = get_user_model()

        # ── 1. Create superuser ──────────────────────────────────────────────
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email    = os.getenv('DJANGO_SUPERUSER_EMAIL', 'anaikarmohammedfuzail57@gmail.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin@fuzail2025')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists — skipping'))

        # ── 2. Create singleton model instances ──────────────────────────────
        # Import here to ensure Django app registry is ready
        from api.models import AboutSection, HeroSection, SeoSettings, SiteSettings

        _, created = HeroSection.objects.get_or_create(id=1)
        if created:
            self.stdout.write(self.style.SUCCESS('HeroSection created'))
        else:
            self.stdout.write(self.style.WARNING('HeroSection already exists — skipping'))

        _, created = AboutSection.objects.get_or_create(id=1)
        if created:
            self.stdout.write(self.style.SUCCESS('AboutSection created'))
        else:
            self.stdout.write(self.style.WARNING('AboutSection already exists — skipping'))

        _, created = SiteSettings.objects.get_or_create(id=1)
        if created:
            self.stdout.write(self.style.SUCCESS('SiteSettings created'))
        else:
            self.stdout.write(self.style.WARNING('SiteSettings already exists — skipping'))

        _, created = SeoSettings.objects.get_or_create(id=1)
        if created:
            self.stdout.write(self.style.SUCCESS('SeoSettings created'))
        else:
            self.stdout.write(self.style.WARNING('SeoSettings already exists — skipping'))

        self.stdout.write(self.style.SUCCESS('\nInitial data setup complete!'))
