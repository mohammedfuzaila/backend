import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_backend.settings")
django.setup()

from api.models import (
    HeroSection, AboutSection, Skill, Project, Experience,
    Service, Testimonial, BlogPost
)

# 1. Projects
projects = [
  {'title': 'Anaikar Infotech', 'description': 'IT solutions company website with modern design.', 'tech_tags': ['HTML', 'CSS', 'JavaScript'], 'category': 'web', 'live_url': 'https://anaikarinfotech-fuzail.netlify.app/', 'github_url': 'https://github.com/mohammedfuzaila/ANAIKAR-INFOTECH', 'is_featured': True},
  {'title': 'Take a Break — Tourism', 'description': 'Tourism website with destination discovery features.', 'tech_tags': ['Bootstrap', 'HTML', 'CSS'], 'category': 'web', 'live_url': 'https://bootstrap-fuzailproject.netlify.app/', 'github_url': 'https://github.com/mohammedfuzaila/BOOTSTRAP-PROJECT', 'is_featured': True},
  {'title': 'PartyPulse Events', 'description': 'Professional event management company website.', 'tech_tags': ['WordPress', 'CSS'], 'category': 'web', 'live_url': 'https://partypulse-fuzailwordpress.netlify.app/', 'github_url': '', 'is_featured': True},
  {'title': 'ModWalk Footwears', 'description': 'Responsive footwear showcase with smooth navigation.', 'tech_tags': ['HTML', 'CSS', 'JavaScript'], 'category': 'web', 'live_url': 'https://modwalkfootwears.netlify.app/', 'github_url': 'https://github.com/mohammedfuzaila/mold-walk-footwear', 'is_featured': False},
  {'title': 'Pernambut Times', 'description': 'Local news and community information portal.', 'tech_tags': ['HTML', 'CSS', 'JavaScript'], 'category': 'web', 'live_url': 'https://pernambuttimes57.netlify.app/', 'github_url': 'https://github.com/mohammedfuzaila/pbt-time-single-file', 'is_featured': False},
  {'title': 'Dreamy Delight', 'description': 'Cake shop ordering platform with visual appeal.', 'tech_tags': ['HTML', 'CSS', 'JavaScript'], 'category': 'web', 'live_url': 'https://dreamydelight.netlify.app/', 'github_url': 'https://github.com/mohammedfuzaila/DREAMY-DELIGHT', 'is_featured': False},
]

for p in projects:
    if not Project.objects.filter(title=p['title']).exists():
        Project.objects.create(**p)

# 2. Testimonials
testimonials = [
  { "name": 'Client Review', "role": 'Business Owner', "company": '', "message": 'Fuzail is an exceptional developer who delivered our project ahead of schedule. His attention to detail and technical expertise exceeded our expectations. Highly recommended!', "rating": 5 },
  { "name": 'Aspirasys Team', "role": 'Management', "company": 'Aspirasys IT Foundation', "message": 'During his tenure, he demonstrated excellent performance, a positive attitude, and strong learning skills. Sincere, punctual, and a great team player.', "rating": 5 },
  { "name": 'Project Client', "role": 'Startup Founder', "company": '', "message": "Fuzail's expertise in full-stack development helped us launch our platform successfully. His communication was excellent, and he provided valuable insights throughout.", "rating": 5 },
  { "name": 'Happy Customer', "role": 'Small Business Owner', "company": '', "message": 'Working with Fuzail was a pleasure. He understood our requirements perfectly and created a beautiful, functional website that our customers love. Professional and reliable!', "rating": 5 },
]

for t in testimonials:
    if not Testimonial.objects.filter(name=t['name']).exists():
        Testimonial.objects.create(**t)

# 3. Skills
skills = [
  { "name": 'React.js', "category": 'frontend', "level": 90, "color": '#61DAFB' },
  { "name": 'JavaScript', "category": 'frontend', "level": 88, "color": '#F7DF1E' },
  { "name": 'Python', "category": 'backend', "level": 88, "color": '#3776AB' },
  { "name": 'Django', "category": 'backend', "level": 85, "color": '#092E20' },
  { "name": 'HTML5', "category": 'frontend', "level": 95, "color": '#E34F26' },
  { "name": 'CSS3', "category": 'frontend', "level": 92, "color": '#1572B6' },
  { "name": 'Tailwind CSS', "category": 'frontend', "level": 88, "color": '#06B6D4' },
  { "name": 'PostgreSQL', "category": 'database', "level": 78, "color": '#336791' },
  { "name": 'Git', "category": 'devops', "level": 88, "color": '#F05032' },
  { "name": 'Figma', "category": 'uiux', "level": 78, "color": '#F24E1E' },
  { "name": 'Next.js', "category": 'frontend', "level": 78, "color": '#000000' },
  { "name": 'Bootstrap', "category": 'frontend', "level": 85, "color": '#7952B3' },
]

for s in skills:
    if not Skill.objects.filter(name=s['name']).exists():
        Skill.objects.create(**s)

# 4. Experience
experience = [
  {
    "type": 'work', "role": 'Full Stack Developer Trainee',
    "company": 'Aspirasys IT Foundation', "duration": '2024 – Present',
    "location": 'Tamil Nadu, India',
    "description": 'Leading development of scalable web applications using modern JavaScript frameworks. Mentoring junior developers and implementing best practices for code quality and performance optimization.',
    "achievements": ['Delivered 7+ projects with 99% client satisfaction', 'Implemented scalable React + Django architecture', 'Mentored junior developers in best practices', 'Reduced page load times by 40%'],
  },
  {
    "type": 'education', "role": 'B.Sc Computer Science',
    "company": 'Islamiah College (Autonomous)', "duration": '2021 – 2024',
    "location": 'Vaniyambadi, Tamil Nadu',
    "description": 'Graduated with strong knowledge in programming, web development, and computer science fundamentals. Developed practical skills through academic projects and teamwork.',
    "achievements": ['Strong foundation in Data Structures & Algorithms', 'Web development academic projects', 'Collaborative teamwork experience'],
  },
]

for e in experience:
    if not Experience.objects.filter(role=e['role']).exists():
        Experience.objects.create(**e)

# 5. Services
services = [
  { "title": 'Full Stack Development', "description": 'End-to-end web applications with React + Django. Scalable, performant, production-ready.', "icon": 'code', "features": ['React / Next.js', 'Django REST API', 'Database Design', 'Deployment'] },
  { "title": 'Frontend Development', "description": 'Pixel-perfect UIs with smooth animations and responsive design for all devices.', "icon": 'monitor', "features": ['React.js', 'Tailwind CSS', 'Framer Motion', 'Responsive'] },
  { "title": 'Backend Development', "description": 'Robust APIs with JWT auth, secure architecture, and scalable database design.', "icon": 'server', "features": ['Django REST', 'JWT Auth', 'PostgreSQL', 'Security'] },
  { "title": 'WordPress Development', "description": 'Custom WordPress sites with unique themes and powerful CMS functionality.', "icon": 'globe', "features": ['Custom Themes', 'WooCommerce', 'SEO Ready', 'Performance'] },
  { "title": 'UI/UX Design', "description": 'Modern user-centric interfaces with Figma prototypes and design systems.', "icon": 'pen-tool', "features": ['Figma Design', 'Design Systems', 'Wireframing', 'User Flows'] },
  { "title": 'SEO & Performance', "description": 'Maximize digital visibility with comprehensive SEO and Core Web Vitals optimization.', "icon": 'trending-up', "features": ['On-Page SEO', 'Core Web Vitals', 'Analytics', 'Schema'] },
]

for s in services:
    if not Service.objects.filter(title=s['title']).exists():
        Service.objects.create(**s)

# 6. Blogs
blogs = [
  { "title": 'Building Scalable React Applications with Django Backend', "slug": 'react-django-scalable', "excerpt": 'Learn how to architect a full-stack application with React on the frontend and Django REST Framework providing a robust API backend.', "tags": ['React', 'Django', 'Full Stack'], "category": 'Development', "read_time": 8, "is_published": True },
  { "title": 'Mastering Tailwind CSS: Building Premium UI Components', "slug": 'tailwind-premium-ui', "excerpt": 'Explore advanced Tailwind CSS techniques to build beautiful, responsive UI components that look premium and professional.', "tags": ['Tailwind', 'CSS', 'UI/UX'], "category": 'Design', "read_time": 6, "is_published": True },
  { "title": 'JWT Authentication: Best Practices for Secure APIs', "slug": 'jwt-auth-best-practices', "excerpt": 'A comprehensive guide to implementing JWT authentication in your APIs with Django REST Framework and best security practices.', "tags": ['Security', 'Django', 'JWT'], "category": 'Security', "read_time": 10, "is_published": True },
]

for b in blogs:
    if not BlogPost.objects.filter(title=b['title']).exists():
        BlogPost.objects.create(**b)

# 7. Hero Section
hero_data = {
  "name": 'Anaikar Mohammed Fuzail',
  "tagline": 'Full Stack Developer',
  "subtitle": 'Crafting web experiences with precision and creativity. I build scalable, elegant digital solutions from concept to deployment.',
  "show_open_to_work": True,
}
if not HeroSection.objects.exists():
    HeroSection.objects.create(**hero_data)

# 8. About Section
about_data = {
  "bio_1": "Hello! I'm Anaikar Mohammed Fuzail, a passionate Full Stack Developer based in Pernambut, Tamil Nadu, India. My journey in web development began with curiosity, which quickly evolved into a deep passion for building innovative, user-centric applications.",
  "bio_2": "I specialize in React, Python, and Django, building complete end-to-end solutions. My approach combines clean code with creative problem-solving—ensuring every project is both functional and aesthetically pleasing.",
  "bio_3": "When I'm not coding, I explore new technologies, contribute to open-source, and share knowledge with the developer community. I believe in continuous learning to deliver cutting-edge solutions.",
  "projects_count": 15,
  "clients_count": 10,
  "years_experience": 2,
  "satisfaction_rate": 99,
  "show_open_to_work": True,
}
if not AboutSection.objects.exists():
    AboutSection.objects.create(**about_data)

print("Database seeded with fallback data successfully!")
