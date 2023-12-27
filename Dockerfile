FROM python:3.12

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Set work directory
WORKDIR /app

# Copy project
COPY . /app
