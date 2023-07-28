from django import forms
from django.core.validators import RegexValidator

from . import models

class EducationForm(forms.ModelForm):

    school_name = forms.CharField(
        label="School Name", min_length=3, max_length=255,
        validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$',
        message="Only letters are allowed!")],
        widget=forms.TextInput(attrs={"placeholder": "School Name"}),
    )

    degree = forms.CharField(
        label="Degree", min_length=3, max_length=255,
        validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$',
        message="Only letters are allowed!")],
        widget=forms.TextInput(attrs={"placeholder": "B.S Computer Science"}),
    )

    start_date = forms.CharField(
        label="Start Date", min_length=3, max_length=255,
        validators=[RegexValidator(r'^[a-zA-ZÀ-ÿ\s]*$',
        message="Only letters are allowed!")],
        widget=forms.TextInput(attrs={"placeholder": "01-07-1960"}),
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

class SkillsForm(forms.ModelForm):

    class Meta:
        model = models.Skill
        exclude = ["resume"]