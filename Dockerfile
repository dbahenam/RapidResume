# Using a Python-based image for simplicity
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project and install Python dependencies
COPY ./RapidResume .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Use Gunicorn for production (example)
#CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
