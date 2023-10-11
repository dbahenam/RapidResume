from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator

from ... import forms
from ... import models

from ...decorators import check_end_status
from ...utils.date_helpers import date_to_datestr, datestr_to_date



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
            'resume_id' : resume_id
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
                'end_status': request.end_status,
                'resume_id' : resume_id
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
        
        # Attempt to get an existing education object for this resume
        try:
            education = models.Education.objects.get(resume=resume)
        except models.Education.DoesNotExist:
            education = None  # No education instance yet for this resume

        form = forms.EducationForm(request.POST, instance=education)

        if form.is_valid():
            if not education:
                # If there was no education object, create one now with the resume association
                education = form.save(commit=False)
                education.resume = resume
                education.save()
            else:
                form.save()
            return redirect('auth:work_experience', resume_id=resume_id)
        else:
            print(form.errors)
            return render(request, 'resume_builder/education.html', {
                'form' : form,
                'end_status' : request.end_status,
                'resume_id' : resume_id,
            })

class WorkExperienceView(BaseFormMixin):
    template_name = 'resume_builder/work-experience.html'
    
    def get(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get previous inputs for this resume related to form
        work_experiences = models.WorkExperience.objects.filter(resume=resume)

        # If empty display empty form, else display existing records
        extra_forms =  0 if work_experiences.exists() else 1
        forms.WorkExperienceFormSet.extra = extra_forms

        formset = forms.WorkExperienceFormSet(queryset=work_experiences)

        return render(request, self.template_name, {
            'formset' : formset,
            'end_status': request.end_status,
            'resume_id' : resume_id,
        })

    def post(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        work_experiences = models.WorkExperience.objects.filter(resume=resume)

        # Filter out completely empty forms
        formset = forms.WorkExperienceFormSet(request.POST, queryset=work_experiences) # Initially a QueryDict
        formset.data = formset.data.copy() # Make the data mutable
        cleaned_forms = [form for form in formset if any(field.value() for field in form)]
        formset.data['form-TOTAL_FORMS'] = len(cleaned_forms)

        if formset.is_valid(): 
            for form in formset:
                if form.has_changed(): # Avoid saving empty forms
                    instance = form.save(commit=False)
                    instance.resume = resume
                    instance.save()
            return redirect('auth:project', resume_id=resume_id)
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id,
        })

class ProjectView(BaseFormMixin):
    template_name = 'resume_builder/project.html'

    def get(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        projects = models.Project.objects.filter(resume=resume)

        # If empty display empty form, else display existing records
        extra_forms = 0 if projects.exists() else 1
        forms.ProjectFormSet.extra = extra_forms

        formset = forms.ProjectFormSet(queryset=projects)

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status, 
            'resume_id' : resume_id
        })

    def post(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        projects = models.Project.objects.filter(resume=resume)

        # Filter out completely empty forms
        formset = forms.ProjectFormSet(request.POST, queryset=projects) # Initially a QueryDict
        formset.data = formset.data.copy() # Make the data mutable
        cleaned_forms = [form for form in formset if any(field.value() for field in form)] # Count non-empty forms
        formset.data['form-TOTAL_FORMS'] = len(cleaned_forms)

        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    instance = form.save(commit=False)
                    instance.resume = resume
                    instance.save()
            return redirect('auth:skill', resume_id=resume_id)
        
        # If the formset isn't valid
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id
        })

class SkillView(BaseFormMixin):
    template_name = 'resume_builder/skill.html'

    def get(self, request, resume_id):
        
        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        skills = models.Skill.objects.filter(resume=resume)
        
        # If empty display empty form, else display existing records
        extra_forms = 0 if skills.exists() else 1
        forms.SkillFormSet.extra = extra_forms

        formset = forms.SkillFormSet(queryset=skills)
        
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id
        })

    def post(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        skills = models.Skill.objects.filter(resume=resume)

        # Filter out completely empty forms
        formset = forms.SkillFormSet(request.POST, queryset=skills)
        formset.data = formset.data.copy() 
        cleaned_forms = [form for form in formset if any(field.value() for field in form)]
        formset.data['form-TOTAL_FORMS'] = len(cleaned_forms)
        
        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    instance = form.save(commit=False)
                    instance.resume = resume
                    instance.save()
            return redirect('auth:certification', resume_id=resume_id)
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id
        })
    
class CertificationView(BaseFormMixin):
    template_name = "resume_builder/certification.html"

    def get(self, request, resume_id):
        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        certifications = models.Certification.objects.filter(resume=resume)

        # If empty display empty form, else display existing records
        extra_forms = 0 if certifications.exists() else 1
        forms.CertificationFormSet.extra = extra_forms

        formset = forms.CertificationFormSet(queryset=certifications)

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id
        })

    def post(self, request, resume_id):
        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        certifications = models.Certification.objects.filter(resume=resume)

        # Filter out completely empty forms
        formset = forms.CertificationFormSet(request.POST, queryset=certifications) # Initially a QueryDict
        formset.data = formset.data.copy() # Make the data mutable
        cleaned_forms = [form for form in formset if any(field.value() for field in form)] # Count non-empty forms
        formset.data['form-TOTAL_FORMS'] = len(cleaned_forms)

        print(formset)

        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    instance = form.save(commit=False)
                    instance.resume = resume
                    instance.save()
            return redirect('auth:language', resume_id=resume_id)
        
        print(formset.errors)
        
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id
        })

class LanguageView(BaseFormMixin):
    template_name = 'resume_builder/language.html'

    # Get associated resume
    def get(self, request, resume_id):
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        languages = models.Language.objects.filter(resume=resume)

        # If empty display empty form, else display existing records
        extra_forms = 0 if languages.exists() else 1
        forms.LanguageFormSet.extra = extra_forms

        formset = forms.LanguageFormSet(queryset=languages)

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id,
        })

    def post(self, request, resume_id):
        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        languages = models.Language.objects.filter(resume=resume)

        # Filter out completely empty forms
        formset = forms.LanguageFormSet(request.POST, queryset=languages) # Initially a QueryDict
        formset.data = formset.data.copy() # Make the data mutable
        cleaned_forms = [form for form in formset if any(field.value() for field in form)] # Count non-empty forms
        formset.data['form-TOTAL_FORMS'] = len(cleaned_forms)

        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    instance = form.save(commit=False)
                    instance.resume = resume
                    instance.save()
            return redirect('resume_builder:auth_preview', resume_id=resume_id)
        
        # If the formset isn't valid, re-render with the existing data and errors
        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id
        })
