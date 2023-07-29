# Use the official Python base image for your desired Python version
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and requirements.txt into the container's working directory
COPY app.py /app/
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Python script will listen (change if needed)
#EXPOSE 5000

# Command to run the Python script (change if your script has a different name)
CMD ["python", "app.py"]
