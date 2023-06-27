FROM python:3.11 AS builder

ARG REDIS_IP
ARG REDIS_PORT
ARG REDIS_PASSWORD
ARG MONGO_URI

ENV REDIS_IP=${REDIS_IP}
ENV REDIS_PORT=${REDIS_PORT}
ENV REDIS_PASSWORD=${REDIS_PASSWORD}
ENV MONGO_URI=${MONGO_URI}

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /code /app

EXPOSE 6420

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6420", "--proxy-headers"]
