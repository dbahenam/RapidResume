# RapidResume

## Overview
RapidResume is a web-based application that simplifies the resume building process for job seekers. It provides an intuitive form-based data collection system and an array of elegant templates to choose from, easing the creation of professional and attractive resumes.

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Django
- MySQL
- Git

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/dbahenam/RapidResume.git
   ```
2. Navigate to the cloned directory and install dependencies:
   ```
   cd RapidResume
   pip install -r requirements.txt
   ```
3. Create a MySQL database for the project and set up your database configuration in settings.py file.

4. Run the server:
   ```
   python manage.py runserver
   ```
## Features

- **User Management System**: Secure registration, login, and profile management.
- **Form-based Data Input**: Intuitive forms for users to input their personal information, skills, work experience, and education.
- **Multiple Resume Templates**: Several professionally designed resume templates for users to choose from.
- **Resume Generation**: Automatic generation of resumes based on user inputs and selected templates.
- **PDF Export**: Resumes can be exported as PDFs for easy sharing and printing.

## Built With

- [Django](https://www.djangoproject.com/): A high-level Python Web framework.
- [MySQL](https://www.mysql.com/): An open-source relational database management system.
- [HTML/CSS](https://www.w3.org/): Used for the frontend and resume templates.
- [xhtml2pdf/WeasyPrint](https://www.xhtml2pdf.com/): Library used for converting the page to a PDF.

## Deployment

RapidResume can be deployed on platforms like [Heroku](https://www.heroku.com/) or [AWS](https://aws.amazon.com/) for easy access and scalability.

## Development Timeline

The development of RapidResume is planned over a four-week period:

- **Week 1**: Design and setup
- **Week 2**: Development of core features
- **Week 3**: Development of the resume generation feature and the template system
- **Week 4**: Testing, debugging, and deploying, with complete documentation provided

## Contributing

Please read [CONTRIBUTING.md](https://github.com/your-account/rapidresume/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/your-account/rapidresume/blob/main/LICENSE.md) file for details.

## Contact

Please feel free to contact us if you have any questions, ideas, or concerns.
