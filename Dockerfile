# Use the official Python image as a base image
FROM python:3.9

ENV PORT 8000
ENV HOST 0.0.0.0
# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS_JSON $SECRET_VALUE
EXPOSE 8000
ENV FLASK_APP=app:create_app()
# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

# Set working directory
WORKDIR $APP_HOME

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code into the container
COPY . .

ENTRYPOINT ["flask", "run"]
