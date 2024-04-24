# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY ./cspm /app
COPY ./requirements.txt /app
COPY ./.aws /root/.aws

RUN rm -rf /app/myapp/iam
COPY ./iam /app/myapp/iam

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install terraform
RUN apt-get update && apt-get install -y gnupg software-properties-common
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor |  tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" |  tee /etc/apt/sources.list.d/hashicorp.list
RUN apt update
RUN apt-get install terraform
# Check that it's installed
RUN terraform --version 

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update

# Add to Path
ENV PATH=~/.local/bin:$PATH
#RUN aws sts get-caller-identity

# Expose the port that the Django app will run on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]