#!/bin/bash

git checkout *
git pull

# Build the RPi driver images
sudo docker build . -f drivers/Dockerfile -t powmr-driver:rpi

# Run detached
sudo docker compose -f docker-compose-rpi.yaml up -d
