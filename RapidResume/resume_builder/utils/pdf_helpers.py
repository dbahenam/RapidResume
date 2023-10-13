from django.core.cache import cache
import pdfkit

def clear_resume_cache(resume_id):
    cache_key = f"resume_{resume_id}"
    cache.delete(cache_key)

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