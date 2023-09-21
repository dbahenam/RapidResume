from django import forms
from django.core.validators import RegexValidator

from . import models

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['contact_number', 'address']

class PersonalDetailsForm(forms.ModelForm):

    class Meta:
        model = models.PersonalDetails
        exclude = ['resume']

class EducationForm(forms.ModelForm):

    school_name = forms.CharField(
        label='School Name',
        max_length=255,
        min_length=2,
        validators=[
            RegexValidator(r'^[a-zA-Z\s]*$', 'Only letters are allowed.'),
        ],
        error_messages={
            'required': 'School name is required.',
        },
        widget=forms.TextInput(attrs={'placeholder': 'University of California San Diego'})
    )

    degree = forms.CharField(
        label='Degree',
        max_length=255,
        min_length=2,
        validators=[
            RegexValidator(r'^[a-zA-Z\s\.]*$', 'Only letters, spaces and periods are allowed.'),
        ],
        error_messages={
            'required': 'Degree is required.',
        },
        widget=forms.TextInput(attrs={'placeholder': 'Electrical Engineering'})
    )

    start_date = forms.DateField(
        label='Start Date',
        input_formats=['%Y-%m-%d'],
        error_messages={
            'required': 'Start date is required.',
            'invalid': 'Invalid date. Expected format (YYYY-MM-DD).',
        },
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )
    
    gpa = forms.FloatField(
        label="GPA", 
        required=False
    )
    
    class Meta:
        model = models.Education
        # fields = "__all__"
        exclude = ["resume"]

class WorkExperienceForm(forms.ModelForm):

    class Meta:
        model = models.WorkExperience
        exclude = ["resume"]


class ProjectForm(forms.ModelForm):

    class Meta:
        model = models.Project
        exclude = ["resume"]

class SkillForm(forms.ModelForm):

    class Meta:
        model = models.Skill
        exclude = ["resume"]


class CertificationForm(forms.ModelForm):

    class Meta:
        model = models.Certification
        exclude = ["resume"]


class LanguageForm(forms.ModelForm):

    class Meta:
        model = models.Language
        exclude = ["resume"]
        
WorkExperienceFormSet = forms.modelformset_factory(models.WorkExperience, form=WorkExperienceForm, extra=0)
ProjectFormSet = forms.modelformset_factory(models.Project, form=ProjectForm, extra=0)
SkillFormSet = forms.modelformset_factory(models.Skill, form=SkillForm, extra=0)
CertificationFormSet = forms.modelformset_factory(models.Certification, form=CertificationForm, extra=0)
LanguageFormSet = forms.modelformset_factory(models.Language, form=LanguageForm, extra=0)

