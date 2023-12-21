# Use the official Google Cloud SDK image as a base image
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest

# Set the working directory
WORKDIR /app

# Copy the secret credentials directly from Secret Manager to credentials.json
RUN gcloud secrets versions access latest --secret=minatku_cloud_storage --project=minatku --format='json' | jq -r '.payload.data' | base64 --decode > credentials.json

# Use the official Python image as a base image
FROM python:3.9

ENV PORT 8000
ENV HOST 0.0.0.0
# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS credentials.json
EXPOSE 8000

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Entry point
CMD ["flask", "run"]
