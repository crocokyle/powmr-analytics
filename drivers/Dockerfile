FROM python:3
LABEL authors="CrocoKyle"
WORKDIR /driver

RUN apt-get update && apt-get install -y dbus
RUN service dbus start
RUN apt-get install -y bluez
RUN service bluetooth start

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .