from django.db import models
from django.contrib.auth.models import User


class HeroSection(models.Model):
    name = models.CharField(max_length=200, default='Anaikar Mohammed Fuzail')
    tagline = models.CharField(max_length=500, default='Full Stack Developer')
    subtitle = models.TextField(default='Crafting web experiences with precision and creativity.')
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    cta_primary_text = models.CharField(max_length=100, default='View Projects')
    cta_secondary_text = models.CharField(max_length=100, default='Download Resume')
    show_open_to_work = models.BooleanField(default=True, help_text='Show the Open to Work badge in the Hero section')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Section'

    def __str__(self):
        return f"Hero - {self.name}"


class AboutSection(models.Model):
    bio_1 = models.TextField(default='')
    bio_2 = models.TextField(default='', blank=True)
    bio_3 = models.TextField(default='', blank=True)
    profile_image = models.ImageField(upload_to='about/', blank=True, null=True)
    projects_count = models.IntegerField(default=15)
    clients_count = models.IntegerField(default=10)
    years_experience = models.IntegerField(default=2)
    satisfaction_rate = models.IntegerField(default=99)
    show_open_to_work = models.BooleanField(default=True, help_text='Show the Open to Work badge in the About section')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Section'

    def __str__(self):
        return 'About Section'


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('tools', 'Tools'),
        ('uiux', 'UI/UX'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=200, blank=True, help_text='Icon name or URL')
    level = models.IntegerField(default=80, help_text='Skill level 0-100')
    color = models.CharField(max_length=20, default='#6C63FF', blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App'),
        ('fullstack', 'Full Stack'),
        ('backend', 'Backend'),
        ('ui', 'UI/UX'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    long_description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url = models.URLField(blank=True, default='')
    github_url = models.URLField(blank=True, default='')
    tech_tags = models.JSONField(default=list, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='web')
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return self.title


class Experience(models.Model):
    TYPE_CHOICES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='work')
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField()
    achievements = models.JSONField(default=list, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.role} at {self.company}"


class Certificate(models.Model):
    title = models.CharField(max_length=300)
    issuer = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    image = models.ImageField(upload_to='certificates/', blank=True, null=True)
    verify_url = models.URLField(blank=True, default='')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return f"{self.title} - {self.issuer}"


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True, default='')
    message = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(default=5)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.company}"


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True, default='')
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    category = models.CharField(max_length=100, default='General')
    read_time = models.IntegerField(default=5, help_text='Read time in minutes')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SocialLink(models.Model):
    platform = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=100, blank=True, default='')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.platform}: {self.url}"


class SeoSettings(models.Model):
    meta_title = models.CharField(max_length=300, default='AMF Portfolio | Full Stack Developer')
    meta_description = models.TextField(default='')
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)
    keywords = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SEO Settings'

    def __str__(self):
        return 'SEO Settings'


class SiteSettings(models.Model):
    show_hero = models.BooleanField(default=True)
    show_about = models.BooleanField(default=True)
    show_skills = models.BooleanField(default=True)
    show_projects = models.BooleanField(default=True)
    show_experience = models.BooleanField(default=True)
    show_services = models.BooleanField(default=True)
    show_certificates = models.BooleanField(default=True)
    show_testimonials = models.BooleanField(default=True)
    show_blog = models.BooleanField(default=True)
    show_contact = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'

    def __str__(self):
        return 'Site Settings'


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='code')
    features = models.JSONField(default=list, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
