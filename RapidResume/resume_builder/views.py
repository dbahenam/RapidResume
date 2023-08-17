from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import JsonResponse

from . import forms
from . import models
from .decorators import check_end_status
from .utils import date_to_datestr, datestr_to_date
from .constants import PROMPTS, CHATGPT_RESPONSE_LIMIT

import os, openai, json
# Create your views here.

def home(request):
    return render(request, "resume_builder/home.html")

def builder(request):
    template_names = ['template1', 'template2']  # update this list with the names of your templates
    template_contents = {}
    for template_name in template_names:
        file_path = os.path.join(settings.BASE_DIR, 'media', 'templates', f'{template_name}_preview.html')
        with open(file_path, 'r') as file:
            template_contents[template_name] = file.read()
    return render(request, 'resume_builder/builder.html', {'template_contents': template_contents})

def set_template(request):
    if request.method == 'POST':
        template_name = request.POST.get('template_name')
        request.session['template_name'] = template_name
        return JsonResponse({'status':'success'}, safe=False)
    else:
        return JsonResponse({'status':'fail'}, safe=False)

def resume_preview(request):
    request.session['end_status'] = True
    return render(request, "resume_builder/resume_preview.html")

def generate_description(request, form_slug):
    # function_descriptions = [
    #     {
    #         'name': 'get_job_description_list',
    #         'description': 
    #         '''
    #             Generate a list of 5 job descriptions based on the job title and company provided. 
    #         ''',
    #         'parameters': {
    #             'type': 'object',
    #             'properties': {
    #                 'description': {
    #                     'type': 'array',
    #                     'items': {
    #                         'type': 'string',
    #                         'description': 'A job description string'
    #                     },
    #                     'description': 'List of job description strings based on a job title and company name'
    #                 }
    #             },
    #         },
    #         'required': ['description']
    #     },
    # ]

    # if request.method == 'POST':
    #     user_input = json.loads(request.body)
    #     prompt = PROMPTS[form_slug].format(**user_input)
        
    #     response = openai.ChatCompletion.create(
    #         model ='gpt-3.5-turbo-0613',
    #         messages =[{'role': 'user', 'content': prompt}],
    #         functions = function_descriptions,
    #         function_call = {'name': 'get_job_description_list'},
    #     )
    #     output = response.choices[0].message
    #     cleaned_output = output.to_dict()['function_call']['arguments']
        cleaned_output = """
        {
        "description": [
            "Design, develop, and test software applications",
            "Collaborate with cross-functional teams to define and implement software requirements",
            "Debug and resolve software defects and issues",
            "Optimize software performance and scalability",
            "Conduct code reviews and provide feedback for continuous improvement"
        ]
        }
        """
        print(cleaned_output)
        cleaned_output = json.loads(cleaned_output)
        return JsonResponse(cleaned_output)

def start_resume_build(request):
    pass

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
        return redirect('/personal_detail')

# Base FormView
@method_decorator(check_end_status, name='dispatch')
class BaseFormView(FormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['end_status'] = self.request.session.get('end_status', False)
        return context

class PersonalDetailView(BaseFormView):
    # Required / Handles GET
    form_class = forms.PersonalDetailsForm
    template_name = 'resume_builder/personal_detail.html'

    # Retrieve data in session if it exists
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        personal_detail_data = self.request.session.get('personal_detail_data', None)
        kwargs['initial'] = personal_detail_data
        return kwargs

    # Required / Handles POST
    success_url = 'education'
    def form_valid(self, form):
        personal_detail_data = form.cleaned_data
        self.request.session['personal_detail_data'] = personal_detail_data
        return super().form_valid(form)

@method_decorator(check_end_status, name='dispatch')
class EducationView(View):
    
    def get(self, request):
        # Retrieve the data from the session if it exists
        education_data = request.session.get('education_data', None)
        if education_data:
            # Convert date strings back to date objects
            education_data['start_date'] = datestr_to_date(education_data['start_date'])
            if education_data['end_date']:
                education_data['end_date'] = datestr_to_date(education_data['end_date'])
        form = forms.EducationForm(initial=education_data)
        return render(request, 'resume_builder/education.html', {
            'form' : form,
            'end_status' : request.end_status
        })
    
    def post(self, request):
        form = forms.EducationForm(request.POST)
        if form.is_valid():
            education_data = form.cleaned_data
            # Convert date objects to strings
            education_data['start_date'] = date_to_datestr(education_data['start_date'])
            if education_data['end_date'] != None:
                education_data['end_date'] = date_to_datestr(education_data['end_date'])
            request.session['education_data'] = education_data
            return redirect("work-experience")
        else:
            return render(request, "resume_builder/education.html", {
                "form" : form,
                'end_status' : request.end_status
            })

class WorkExperienceView(BaseFormView):
    # Required / Handles GET
    form_class = forms.WorkExperienceForm
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

class SkillView(BaseFormView):
    # Required / Handles GET
    form_class = forms.SkillForm
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
    
class CertificationView(BaseFormView):
    # Required / Handles GET
    form_class = forms.CertificationForm
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

class ProjectView(BaseFormView):
    # Required / Handles GET
    form_class = forms.ProjectForm
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

class LanguageView(BaseFormView):
    # Required / Handles GET
    form_class = forms.LanguageForm
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

