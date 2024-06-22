FROM python:3
LABEL authors="CrocoKyle"
WORKDIR /driver

RUN apt-get update && apt-get install -y \
    bluez \
    dbus

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN service dbus start
RUN service bluetooth start

COPY .. .