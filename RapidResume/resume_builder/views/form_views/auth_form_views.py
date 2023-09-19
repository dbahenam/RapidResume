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
        # If no work_experiences, create an unsaved one for display.
        if not work_experiences.exists():
            new_work_experience = models.WorkExperience(resume=resume)
            work_experiences = [new_work_experience]
            extra_forms = 1  # This ensures one empty form is created.
        else:
            work_experiences = list(work_experiences)
            extra_forms = 0  # No extra empty forms when there are existing work_experiences.
        # if not work_experiences.exists():
        #     # Create a new unsaved WorkExperience instance
        #     new_work_experience = models.WorkExperience(resume=resume)
        #     # Create a new queryset containing the new instance
        #     work_experiences = models.WorkExperience.objects.filter(pk__in=[None])
        #     work_experiences._result_cache = [new_work_experience]
        # formset = forms.WorkExperienceFormSet(queryset=work_experiences)
        WorkExperienceFormSet = modelformset_factory(models.WorkExperience, form=forms.WorkExperienceForm, extra=extra_forms)
        formset = WorkExperienceFormSet(queryset=models.WorkExperience.objects.filter(pk__in=[w.pk for w in work_experiences]))

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status,
            'resume_id' : resume_id,
        })

    def post(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(pk=resume_id, user=request.user)

        # Get associated forms
        work_experiences = models.WorkExperience.objects.filter(resume=resume)
        formset = forms.WorkExperienceFormSet(request.POST, queryset=work_experiences)

        # print(formset)

        if formset.is_valid():
            # Using formsets makes this convenient -- it can create/update/delete instances
            instances = formset.save(commit=False)
            for instance in instances:
                instance.resume = resume  # setting foreign key relationship
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
        if not projects.exists():
            # Create an empty form
            empty_form = forms.ProjectForm()
            # Create a formset with the empty form
            formset = forms.ProjectFormSet(queryset=projects)
            formset.forms.append(empty_form)
        else:
            formset = forms.ProjectFormSet(queryset=projects)

        return render(request, self.template_name, {
            'formset': formset,
            'end_status': request.end_status, 
            'resume_id' : resume_id
        })

    def post(self, request, resume_id):

        # Get associated resume
        resume = models.Resume.objects.get(resume=resume_id)

        # Get associated forms
        projects = models.Project.objects.filter(resume=resume)
        formset = forms.ProjectFormSet(queryset=projects)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
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
