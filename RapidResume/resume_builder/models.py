from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

class Template(models.Model):
    name = models.CharField(max_length=255)
    html_file = models.FileField(upload_to='templates')
    css_file = models.FileField(upload_to='templates')
    # preview_image = models.ImageField(upload_to='template_previews', null=True, blank=True)

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # sessions, id, time
    title = models.CharField(max_length=255)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    major = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True) # makemigrations, migrate

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    proficiency_level = models.CharField(max_length=255)  # or use IntegerField with choices

class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuing_org = models.CharField(max_length=255)
    date_issued = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    cert_url = models.URLField(null=True, blank=True)

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    project_url = models.URLField(null=True, blank=True)

class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    proficiency_level = models.CharField(max_length=255)


