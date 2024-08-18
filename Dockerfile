# Dockerfile

# Use the official Python image as a base
FROM python:3.11

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project directory to the container
COPY . /app/

# Expose the port your Django app runs on
EXPOSE 8000

# Define the command to start the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
