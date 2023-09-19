from django.http import JsonResponse
from ..constants import PROMPTS, FUNCTION_DESCRIPTIONS

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