#!/bin/bash

git checkout *
git checkout async-drivers
git pull

# Build the RPi driver images
sudo docker build . -f drivers/inverter/Dockerfile -t powmr-driver:rpi
sudo docker build . -f driver/Dockerfile -t powmr-driver:rpi

# Run detached
sudo docker compose -f docker-compose-rpi.yaml up -d