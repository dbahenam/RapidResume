from django.shortcuts import HttpResponse
from django.template.loader import get_template

from ..utils.pdf_helpers import *

def download_resume_pdf(request, resume_id=None):
    # if resume_id:

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