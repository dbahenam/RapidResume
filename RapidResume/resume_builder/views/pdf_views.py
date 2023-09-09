from django.shortcuts import HttpResponse
from django.template.loader import get_template

import pdfkit


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