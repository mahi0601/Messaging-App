# Dockerfile

# Use the official Python image as a base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "myproject.asgi:application"]
