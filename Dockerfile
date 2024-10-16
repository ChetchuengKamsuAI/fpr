# Use Python 3.9.13 image as the base image
FROM python:3.9.13

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip to the latest version to avoid the warning
RUN python -m pip install --upgrade pip

# Install the dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Ensure the necessary port (commonly 8000) is exposed for web traffic
EXPOSE 8000

# Set environment variable for the port, default to 8000 if not set
ENV PORT 8000

# Define the entry point for the container to run your app (update if needed)
CMD ["python", "login.py"]
