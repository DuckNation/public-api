# Use an official Python runtime as the base image
FROM python:3.11

ARG REDIS_IP
ARG REDIS_PORT
ARG REDIS_PASSWORD
ARG MONGO_URI

ENV REDIS_IP=${REDIS_IP}
ENV REDIS_PORT=${REDIS_PORT}
ENV REDIS_PASSWORD=${REDIS_PASSWORD}
ENV MONGO_URI=${MONGO_URI}

# Rest of your Dockerfile


# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install the dependencies
COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the entire application code to the container
COPY . /code

# Expose the port that your FastAPI application listens on
EXPOSE 6420

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6420", "--proxy-headers"]
