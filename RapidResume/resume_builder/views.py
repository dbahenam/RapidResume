from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from . forms import EducationForm, WorkExperienceForm, SkillForm, CertificationForm, ProjectForm, LanguageForm, PersonalDetailsForm
from .utils import date_to_datestr, datestr_to_date

# Create your views here.

def home(request):
    return render(request, "resume_builder/home.html")

def builder(request):
    return render(request, "resume_builder/builder.html")

def resume_preview(request):
    return render(request, "resume_builder/resume_preview.html")

def new_resume(request):
    # if user is not logged in, option to login
    # "log in to save previous resume progress or"
    # "replace and start over"
    if request.user.is_authenticated:
        # Do something for authenticated users.
        # save resume, create model
        return render(request, 'authenticated_template.html')
    else:
        # Clear session
        request.session.clear()
        return redirect('/education')


class UserProfileView(FormView):
    # Required / Handles GET
    form_class = PersonalDetailsForm
    template_name = 'resume_builder/user_profile.html'

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        skill_data = self.request.session.get('skill_data', None)
        kwargs['initial'] = skill_data
        return kwargs

    # Required / Handles POST
    success_url = 'certification'
    def form_valid(self, form):
        skill_data = form.cleaned_data
        self.request.session['skill_data'] = skill_data
        return super().form_valid(form)




class EducationView(View):
    
    def get(self, req):
        # Retrieve the data from the session if it exists
        education_data = req.session.get('education_data', None)
        if education_data:
            # Convert date strings back to date objects
            education_data['start_date'] = datestr_to_date(education_data['start_date'])
            if education_data['end_date']:
                education_data['end_date'] = datestr_to_date(education_data['end_date'])
        form = EducationForm(initial=education_data)
        return render(req, 'resume_builder/education.html', {
            'form' : form
        })
    
    def post(self, req):
        form = EducationForm(req.POST)
        if form.is_valid():
            education_data = form.cleaned_data
            # Convert date objects to strings
            education_data['start_date'] = date_to_datestr(education_data['start_date'])
            if education_data['end_date'] != None:
                education_data['end_date'] = date_to_datestr(education_data['end_date'])
            req.session['education_data'] = education_data
            return redirect("work-experience")
        else:
            return render(req, "resume_builder/education.html", {
                "form" : form
            })

class WorkExperienceView(FormView):
    # Required / Handles GET
    form_class = WorkExperienceForm
    template_name = 'resume_builder/work-experience.html'

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        work_experience_data = self.request.session.get('work_experience_data', None)
        if work_experience_data:
            # Convert date strings back to date objects
            work_experience_data['start_date'] = datestr_to_date(work_experience_data['start_date'])
            if work_experience_data['end_date']:
                work_experience_data['end_date'] = datestr_to_date(work_experience_data['end_date'])
        kwargs['initial'] = work_experience_data
        return kwargs

    # Required / Handles POST
    success_url = 'skill'
    def form_valid(self, form):
        work_experience_data = form.cleaned_data
        # Convert date objects back to strings
        work_experience_data['start_date'] = date_to_datestr(work_experience_data['start_date'])
        if work_experience_data['end_date'] != None:
            work_experience_data['end_date'] = date_to_datestr(work_experience_data['end_date'])
        self.request.session['work_experience_data'] = work_experience_data
        return super().form_valid(form)


class SkillView(FormView):
    # Required / Handles GET
    form_class = SkillForm
    template_name = 'resume_builder/skill.html'

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        skill_data = self.request.session.get('skill_data', None)
        kwargs['initial'] = skill_data
        return kwargs

    # Required / Handles POST
    success_url = 'certification'
    def form_valid(self, form):
        skill_data = form.cleaned_data
        self.request.session['skill_data'] = skill_data
        return super().form_valid(form)
    

class CertificationView(FormView):
    # Required / Handles GET
    form_class = CertificationForm
    template_name = "resume_builder/certification.html"

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        certification_data = self.request.session.get('certification_data', None)
        if certification_data:
            # Convert date strings back to date objects
            certification_data['date_issued'] = datestr_to_date(certification_data['date_issued'])
            if certification_data['expiration_date']:
                certification_data['expiration_date'] = datestr_to_date(certification_data['expiration_date'])
        kwargs['initial'] = certification_data
        return kwargs

    # Required / Handles POST
    success_url = 'project'
    def form_valid(self, form):
        certification_data = form.cleaned_data
        certification_data['date_issued'] = date_to_datestr(certification_data['date_issued'])
        if certification_data['expiration_date']:
            certification_data['expiration_date'] = date_to_datestr(certification_data['expiration_date'])
        self.request.session['certification_data'] = certification_data
        return super().form_valid(form)

class ProjectView(FormView):
    # Required / Handles GET
    form_class = ProjectForm
    template_name = 'resume_builder/project.html'

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_data = self.request.session.get('project_data', None)
        if project_data:
            # Convert date strings back to date objects
            project_data['start_date'] = datestr_to_date(project_data['start_date'])
            if project_data['end_date']:
                project_data['end_date'] = datestr_to_date(project_data['end_date'])
        kwargs['initial'] = project_data
        return kwargs
    
    # Required / Handles POST
    success_url = 'language'
    def form_valid(self, form):
        project_data = form.cleaned_data
        # Convert date objects to strings
        project_data['start_date'] = date_to_datestr(project_data['start_date'])
        if project_data['end_date']:
            project_data['end_date'] = date_to_datestr(project_data['end_date'])
        self.request.session['project_data'] = project_data
        return super().form_valid(form)

class LanguageView(FormView):
    # Required / Handles GET
    form_class = LanguageForm
    template_name = 'resume_builder/language.html'

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        language_data = self.request.session.get('language_data', None)
        kwargs['initial'] = language_data
        return kwargs
    
    # Required / Handles POST
    success_url = 'resume_preview'
    def form_valid(self, form):
        language_data = form.cleaned_data
        self.request.session['language_data'] = language_data
        return super().form_valid(form)

