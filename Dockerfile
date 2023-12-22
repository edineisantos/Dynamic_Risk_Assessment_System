# Use jupyter/base-notebook
FROM jupyter/base-notebook:python-3.8.13

# Make the directory for the project files
RUN mkdir /home/jovyan/work/Dynamic_Risk_Assessment_System

# Set the working directory to /home/jovyan/work
WORKDIR /home/jovyan/work/Dynamic_Risk_Assessment_System

# Copy the current directory contents into the container
COPY . /home/jovyan/work/Dynamic_Risk_Assessment_System

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install git and cron
USER root
RUN apt-get update && apt-get install -y git cron

# Expose the ports Jupyter and other services will run on
EXPOSE 8888
EXPOSE 8889
EXPOSE 8890

# Switch back to the non-root user
USER jovyan


