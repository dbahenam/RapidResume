from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from ... import forms
from ... import models

from ...decorators import check_end_status
from ...utils.date_helpers import date_to_datestr, datestr_to_date

from ...constants import PROMPTS, FUNCTION_DESCRIPTIONS

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

@method_decorator(check_end_status, name='dispatch')
class BaseFormMixin(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = kwargs  # Start with provided keyword arguments
        context['end_status'] = self.request.session.get('end_status', False)
        return context

class PersonalDetailView(BaseFormMixin):
    def get(self, request, resume_id):
        try:
            resume = models.Resume.objects.get(pk=resume_id, user=request.user)
        except models.Resume.DoesNotExist:
            return HttpResponseNotFound("Resume not found.")
        
        # Try to get data if it exists, set empty form if it doesn't
        try:
            personal_detail = models.PersonalDetails.objects.get(resume=resume)
            form = forms.PersonalDetailsForm(instance=personal_detail)
        except models.PersonalDetails.DoesNotExist:
            form = forms.PersonalDetailsForm()

        return render(request, 'resume_builder/personal_detail.html', {
            'form': form,
            'end_status': request.end_status,
        })

    def post(self, request, resume_id):
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Check if data already exists for this resume
        personal_detail, created = models.PersonalDetails.objects.get_or_create(resume=resume)

        form = forms.PersonalDetailsForm(request.POST, instance=personal_detail)

        if form.is_valid():
            form.save()
            return redirect('auth:education', resume_id=resume_id)
        else:
            return render(request, "resume_builder/personal_detail.html", {
                "form": form,
                'end_status': request.end_status
            })

class EducationView(BaseFormMixin):
    def get(self, request, resume_id):
        try:
            resume = models.Resume.objects.get(pk=resume_id, user=request.user)
        except models.Resume.DoesNotExist:
            return HttpResponseNotFound("Resume not found.")
        
        # Try to get data if it exists, set empty form if it doesn't
        try:
            education = models.Education.objects.get(resume=resume)
            form = forms.EducationForm(instance=education)
        except models.Education.DoesNotExist:
            form = forms.EducationForm()
        
        return render(request, 'resume_builder/education.html', {
            'form' : form,
            'end_status' : request.end_status,
            'resume_id' : resume_id
        })

    def post(self, request, resume_id):
        print(request.POST)
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)
        print("resume: ", resume)
        # Check if data already exists for this resume
        education, created = models.Education.objects.get_or_create(resume=resume)
        print("after education")
        form = forms.EducationForm(request.POST, instance=education)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('auth:work_experience', resume_id=resume_id)
        else:
            print(form.errors)
            return render(request, 'resume_builder/education.html', {
                'form' : form,
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
            return redirect('unauth:project')
        
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
            return redirect('unauth:skill')
        
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
            return redirect('unauth:certification')
        
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
            return redirect('unauth:language')
        
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
            return redirect('resume_builder:preview_resume') 
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status
        })