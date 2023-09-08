from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import JsonResponse

from . import forms
from . import models
from .decorators import check_end_status
from .utils import date_to_datestr, datestr_to_date
from .constants import PROMPTS, FUNCTION_DESCRIPTIONS

from django.template.loader import get_template

import pdfkit

import os, openai, json

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
    print(request.session.items())
    return render(request, "resume_builder/resume_preview.html")

def generate_description(request, form_slug):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    function_descriptions = FUNCTION_DESCRIPTIONS
    if request.method == 'POST':
        user_input = json.loads(request.body)
        prompt = PROMPTS[form_slug].format(**user_input)
        
        response = openai.ChatCompletion.create(
            model ='gpt-3.5-turbo-0613',
            messages =[{'role': 'user', 'content': prompt}],
            functions = function_descriptions,
            function_call = {'name': form_slug},
        )
        output = response.choices[0].message
        cleaned_output = output.to_dict()['function_call']['arguments']
        # print(cleaned_output)
        cleaned_output = json.loads(cleaned_output)
        # cleaned_output = SAMPLE_CHATGPT_OUTPUT
        return JsonResponse(cleaned_output)

def prepare_descriptions(session_data):

    def split_description(description):
        return description.replace('\r\n', '\n').split('\n')

    keys_with_description = ['education_data', 'work_experience_data', 'project_data']  # Extend this list as needed

    # Loop through each key and process the descriptions
    for key in keys_with_description:
        if key in session_data:
            for item in session_data[key]:
                if 'description' in item:
                    item['description'] = split_description(item['description'])

    return session_data

def start_resume_build(request):
    context = dict(request.session.items())
    print(request.session.items())
    return render(request, 'resume_template.html', context)

def render_to_pdf(html_content):
    # Convert HTML to PDF using pdfkit
    pdf = pdfkit.from_string(html_content, False)  # Second argument False means it will return the PDF as bytes

    if pdf:
        return pdf
    return None

def download_resume_pdf(request):
    # Fetch the same data from the session
    context = dict(request.session.items())
    template = get_template('includes/resume_body.html')
    html = template.render(context)
    
    pdf = render_to_pdf(html)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Resume_%s.pdf" %("12341231")
        content = "attachment; filename='%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Error generating PDF")

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

@method_decorator(check_end_status, name='dispatch')
class BaseFormMixin(View):
    def get_context_data(self, **kwargs):
        context = kwargs  # Start with provided keyword arguments
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

class EducationView(BaseFormMixin):
    
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

class WorkExperienceView(BaseFormMixin):
    template_name = 'resume_builder/work-experience.html'
    
    def get(self, request):

        work_experience_data = self.request.session.get('work_experience_data', None)

        if isinstance(work_experience_data, dict): # Remove later
            work_experience_data = [work_experience_data]
        
        # Create formset witht he data from session
        formset = forms.WorkExperienceFormSet(initial=work_experience_data)

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

    def post(self, request):
        formset = forms.WorkExperienceFormSet(request.POST)
        if formset.is_valid():
            serialized_data= []
            for form in formset:
                if form.has_changed():  # This will be False for empty forms
                    work_experience_data = form.cleaned_data
                    work_experience_data['start_date'] = date_to_datestr(work_experience_data['start_date'])
                    if work_experience_data['end_date']:
                        work_experience_data['end_date'] = date_to_datestr(work_experience_data['end_date'])
                    serialized_data.append(work_experience_data)
            self.request.session['work_experience_data'] = serialized_data
            # print(self.request.session['work_experience_data'])
            return redirect('/project')
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

class ProjectView(BaseFormMixin):
 
    template_name = 'resume_builder/project.html'

    # Retrieve data in session if it exists
    def get(self, request):
        project_data = self.request.session.get('project_data', [])
        if isinstance(project_data, dict): # Remove later
            project_data = [project_data]
        
        # Create formset with the data from the session, or empty if there's none
        formset = forms.ProjectFormSet(initial=project_data)

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

    def post(self, request):
        formset = forms.ProjectFormSet(request.POST)

        if formset.is_valid():
            serialized_data = []
            for form in formset:
                if form.has_changed():  # This will be False for empty forms
                    project_data = form.cleaned_data
                    project_data['start_date'] = date_to_datestr(project_data['start_date'])
                    if project_data['end_date']:
                        project_data['end_date'] = date_to_datestr(project_data['end_date'])
                    serialized_data.append(project_data)
            self.request.session['project_data'] = serialized_data
            return redirect('/skill')
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })


class SkillView(BaseFormMixin):
    template_name = 'resume_builder/skill.html'

    def get(self, request):
        skill_data = self.request.session.get('skill_data', [])
        if isinstance(skill_data, dict):
            skill_data = [skill_data]
        
        # Create formset with the data from the session, or empty if there's none
        formset = forms.SkillFormSet(initial=skill_data)
        
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

    def post(self, request):
        formset = forms.SkillFormSet(request.POST)

        if formset.is_valid():
            serialized_data = []
            for form in formset:
                if form.has_changed():  # This will be False for empty forms
                    skill_data = form.cleaned_data
                    serialized_data.append(skill_data)
            self.request.session['skill_data'] = serialized_data
            return redirect('/certification')
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })
    
class CertificationView(BaseFormMixin):
    template_name = "resume_builder/certification.html"

    def get(self, request):
        certification_data = self.request.session.get('certification_data', [])
        if isinstance(certification_data, dict):
            certification_data = [certification_data]
        
        # Create formset with the data from the session, or empty if there's none
        formset = forms.CertificationFormSet

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

    def post(self, request):
        formset = forms.CertificationFormSet(request.POST)

        if formset.is_valid():
            serialized_data = []
            for form in formset:
                if form.has_changed():
                    certification_data = form.cleaned_data
                    certification_data['date_issued'] = date_to_datestr(certification_data['date_issued'])
                    if certification_data['expiration_date']:
                        certification_data['end_date'] = date_to_datestr(certification_data['expiration_date'])
                    serialized_data.append(certification_data)
            self.request.session['certification_data'] = serialized_data
            return redirect('/language')
        
        # If the formset isn't valid, re-render with the existing data and errors
        print(formset.errors)
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

class LanguageView(BaseFormMixin):
    template_name = 'resume_builder/language.html'

    def get(self, request):
        language_data = self.request.session.get('language_data', [])
        if isinstance(language_data, dict):
            language_data = [language_data]
        
        # Create formset with the data from the session, or empty if there's none
        formset = forms.LanguageFormSet

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })

    def post(self, request):
        formset = forms.LanguageFormSet(request.POST)

        if formset.is_valid():
            serialized_data = []
            for form in formset:
                if form.has_changed():
                    language_data = form.cleaned_data
                    serialized_data.append(language_data)
            self.request.session['language_data'] = serialized_data
            return redirect('/resume_preview')
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })
