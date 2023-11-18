# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY . .

# Install Pipenv and any dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install 

# Copy the rest of your action's code to the working directory


# Run the script when the container launches
# Replace `your_script.py` with the script you want to run
CMD ["pipenv", "run", "python", "/app/main.py"]
