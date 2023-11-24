#!/bin/bash

git checkout *
git pull

# Build the RPi images
sudo docker build . -f driver/Dockerfile -t powmr-driver:rpi

# Enable Docker service on startup
sudo systemctl enable docker

# Run detached
sudo docker compose -f docker-compose-rpi.yaml up -d