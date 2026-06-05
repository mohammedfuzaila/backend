from django.contrib import admin
from .models import (
    HeroSection, AboutSection, Skill, Project, Experience,
    Certificate, Testimonial, BlogPost, ContactMessage,
    SocialLink, SeoSettings, SiteSettings, Service
)

admin.site.register(HeroSection)
admin.site.register(AboutSection)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certificate)
admin.site.register(Testimonial)
admin.site.register(BlogPost)
admin.site.register(ContactMessage)
admin.site.register(SocialLink)
admin.site.register(SeoSettings)
admin.site.register(SiteSettings)
admin.site.register(Service)
