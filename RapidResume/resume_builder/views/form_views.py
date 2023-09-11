from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from .. import forms
from .. import models

from ..decorators import check_end_status
from ..utils.date_helpers import date_to_datestr, datestr_to_date

from ..constants import PROMPTS, FUNCTION_DESCRIPTIONS

import os, openai, json

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
        print("cert data: ", certification_data)
        if isinstance(certification_data, dict):
            certification_data = [certification_data]
        
        # Create formset with the data from the session, or empty if there's none
        formset = forms.CertificationFormSet(initial=certification_data)

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
        formset = forms.LanguageFormSet(initial=language_data)

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
