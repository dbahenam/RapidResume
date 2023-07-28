from django.shortcuts import render, redirect, get_object_or_404
from . forms import EducationForm, WorkExperienceForm, SkillsForm

# Create your views here.

def home(req):
    return render(req, "resume_builder/home.html")

def builder(req):
    return render(req, "resume_builder/builder.html")

def education(req):
    if req.method == "POST":
        form = EducationForm(req.POST)
        if form.is_valid():
            #form.save()
            return redirect('work-experience')
    else:
        form = EducationForm()
    return render(req, "resume_builder/education.html", {
        "form" : form
    })

def work_experience(req):
    if req.method == "POST":
        form = WorkExperienceForm(req.POST)
        if form.is_valid():
            #form.save()
            return redirect('skills')
    else:
        form = WorkExperienceForm()
    return render(req, "resume_builder/work-experience.html", {
        "form" : form
    })

def skills(req):
    if req.method == "POST":
        form = SkillsForm(req.POST)
        if form.is_valid():
            #form.save()
            return redirect('certifications')
    else:
        form = SkillsForm()
    return render(req, "resume_builder/skills.html", {
        "form" : form
    })

def certifications(req):
    pass