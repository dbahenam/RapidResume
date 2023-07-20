from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

class Template(models.Model):
    template_name = models.CharField(max_length=255)

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
 
class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)



