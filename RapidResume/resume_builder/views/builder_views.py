from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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

def preview_resume(request):
    request.session['end_status'] = True
    print(request.session.items())
    context = dict(request.session.items())
    # return render(request, 'resume_template.html', context)
    return render(request, 'resume_builder/resume_preview.html')

