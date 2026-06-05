from django.contrib import admin
from .models import (
    HeroSection, AboutSection, Skill, Project, Experience,
    Certificate, Testimonial, BlogPost, ContactMessage,
    SocialLink, SeoSettings, SiteSettings, Service
)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline', 'is_active', 'updated_at')
    list_editable = ('is_active',)

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'years_experience', 'is_active', 'updated_at')
    list_editable = ('is_active',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('level', 'order', 'is_active')
    search_fields = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'order', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'order', 'is_active')
    search_fields = ('title', 'description')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'type', 'duration', 'order', 'is_active')
    list_filter = ('type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('role', 'company')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'date', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'issuer')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'company', 'rating', 'order', 'is_active')
    list_filter = ('rating', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'company')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'created_at')
    list_filter = ('category', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('platform',)

@admin.register(SeoSettings)
class SeoSettingsAdmin(admin.ModelAdmin):
    list_display = ('meta_title', 'updated_at')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'maintenance_mode', 'updated_at')
    list_editable = ('maintenance_mode',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
