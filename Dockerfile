# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY ./iam /app/iam/
COPY ./cspm /app
COPY ./requirements.txt /app

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Django app will run on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]