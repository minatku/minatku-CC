# Use the official Python image as a base image
FROM python:3.9

ENV PORT 8000
ENV HOST 0.0.0.0
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
