# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Upgrade pip and install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN python -m venv /app/venv

# Install system dependencies, including ffmpeg, ffprobe, espeak, and Python development headers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    espeak \
    python3-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Activate the virtual environment and upgrade pip within it
RUN /app/venv/bin/pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt within the virtual environment
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py


# # Activate the virtual environment and install system dependencies
# # Use the venv's pip to install packages into the virtual environment
# RUN /app/venv/bin/pip install --upgrade pip && \
#     apt-get update && \
#     apt-get install -y build-essential gcc cmake ffmpeg espeak libespeak-dev espeak-ng libespeak-ng1 libespeak-ng-dev git wget bash && \
#     apt-get install -y python3-dev python3-pip python3-wheel pkg-config && \
#     rm -rf /var/lib/apt/lists/*


# Run main.py when the container launches
CMD ["gunicorn", "run", "--host=0.0.0.0"]