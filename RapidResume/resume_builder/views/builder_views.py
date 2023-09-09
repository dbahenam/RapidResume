from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings

import os


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

def start_resume_build(request):
    context = dict(request.session.items())
    print(request.session.items())
    return render(request, 'resume_template.html', context)

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