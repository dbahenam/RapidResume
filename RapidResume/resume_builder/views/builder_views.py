from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
import json 

from ..models import Resume

def resume_dashboard(request):
    if request.user.is_authenticated:
        resumes = Resume.objects.filter(user=request.user)
    else:
        resumes = None
    return render(request, 'resume_builder/builder.html', {'resumes' : resumes})

@require_POST
def create_new_resume(request):
    resume_title = json.loads(request.body)['resumeTitle']
    if request.user.is_authenticated:
        new_resume_obj = Resume(user=request.user, title=resume_title)
        new_resume_obj.save()
        redirect_url = reverse('auth:personal_detail')
        return JsonResponse({'status': 'success', 'redirect_url': redirect_url})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unauthenticated User'})

def resume_preview(request, resume_id=None):
    request.session['end_status'] = True
    if resume_id:
        cache_key = f"resume_{resume_id}"
        cached_resume = cache.get(cache_key)
        # print(vars(cache.get(cache_key)))
        if not cached_resume:
            resume_data = get_object_or_404(Resume.objects.prefetch_related(
                'personaldetails',
                'education_set',
                'workexperience_set',
                'project_set',
                'skill_set',
                'certification_set',
                'language_set',
            ), pk=resume_id, user=request.user)
            cache.set(cache_key, resume_data, 1800)  # cache for 30 minutes
        else:
            resume_data = cached_resume

        return render(request, 'resume_builder/resume_preview.html', {
            'resume_id':resume_id,
            'resume_data': resume_data
        })
    else:
        resume_data = dict(request.session.items())
        print(resume_data)
        return render(request, 'resume_builder/resume_preview.html', {
            'resume_data': resume_data
        })

