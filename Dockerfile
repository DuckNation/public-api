# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Expose the port that your FastAPI application listens on
EXPOSE 6420

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6420"]
