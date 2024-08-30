# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies, including wget and bash
RUN apt-get update && \
    apt-get install -y build-essential gcc cmake ffmpeg espeak libespeak-dev espeak-ng libespeak-ng1 libespeak-ng-dev git wget bash && \
    apt-get install -y python3-dev python3-pip python3-wheel pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install setuptools using pip
RUN pip install setuptools

# Install numpy first to avoid binary incompatibility issues
RUN pip install numpy==1.25.0

# Install aeneas
RUN pip install aeneas==1.7.3

# Copy the current directory contents into the container at /app
COPY . /app

# Install other Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py

# Run main.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]