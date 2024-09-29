# Dockerfile for NeoOrrery

# Use the official Python image as a base
FROM python:3.12.6-slim

# Set environment variables to reduce buffer size issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the working directory
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /usr/src/app/

# Expose the port that the Django app runs on
EXPOSE 8000

# Run the application server
CMD ["python", "NeoOrreryProject/manage.py", "runserver", "0.0.0.0:8000"]

