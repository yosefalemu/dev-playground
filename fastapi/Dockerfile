FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip --default-timeout=200 install --no-cache-dir -r requirements.txt
