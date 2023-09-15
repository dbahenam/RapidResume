from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json 

from ..models import Resume

def builder(request):
    if request.user.is_authenticated:
        resumes = Resume.objects.filter(user=request.user)
    else:
        resumes = None
    return render(request, 'resume_builder/builder.html', {'resumes' : resumes})

def start_resume_build(request):
    context = dict(request.session.items())
    print(request.session.items())
    return render(request, 'resume_template.html', context)

@require_POST
def new_resume(request):
    resume_title = json.loads(request.body)['resumeTitle']
    if request.user.is_authenticated:
        new_resume_obj = Resume(user=request.user, title=resume_title)
        new_resume_obj.save()
        return JsonResponse({'status': 'success', 'redirect_url': '/personal_detail'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unauthenticated User'})

def resume_preview(request):
    request.session['end_status'] = True
    print(request.session.items())
    return render(request, "resume_builder/resume_preview.html")
