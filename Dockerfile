# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . /app

# Expose port 8080 for Flask
EXPOSE 8080

# Define the command to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "flask_app:app"]