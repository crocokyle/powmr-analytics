FROM python:3
LABEL authors="CrocoKyle"
WORKDIR /driver

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .