# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to avoid buffering and to set UTF-8
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Install the necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    unixodbc-dev \
    curl \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
