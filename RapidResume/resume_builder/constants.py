PROMPTS = {
    'project' : 'Generate a list of 5 resume bullet points to describe a {first_input} project that uses the following technologies {second_input}. ',
    'education' : 'Describe an academic experience at {first_input} with a major in {second_input}. Mention any notable achievements related to the {second_input}. ',
    'work-experience' : "Generate a list of 5 resume bullet points describing the role and responsibilities of a {first_input} at {second_input}."
}

CHATGPT_RESPONSE_LIMIT = "Limit your response to 5 bulltet points."

FUNCTION_DESCRIPTIONS = [
        {
            'name': 'work-experience',
            'description': 
            '''
                Generate a list of 5 job descriptions based on the job title and company provided. 
            ''',
            'parameters': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'A job description string'
                        },
                        'description': 'List of job description strings based on a job title and company name'
                    }
                },
            },
            'required': ['description']
        },
        {
            'name': 'project',
            'description':
            '''
                Generate a list of 5 project descriptions based on the project name and the technologies used in the project'
            ''',
            'parameters': {
                'type': 'object',
                'properties': {
                    'description': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'description': 'A project description string'
                        },
                        'description': 'List of project description strings based on the project name and the technologies used in the project'
                    }
                }
            }
        },
    ]

SAMPLE_CHATGPT_OUTPUT = """
                        {
                            "description": [
                                "Design, develop, and test software applications",
                                "Collaborate with cross-functional teams to define and implement software requirements",
                                "Debug and resolve software defects and issues",
                                "Optimize software performance and scalability",
                                "Conduct code reviews and provide feedback for continuous improvement"
                            ]
                        }
                        """

STATE_CHOICES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]
