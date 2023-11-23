#!/bin/bash

# Uninstall old Docker
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get>

# Add Docker's official GPG key:
sudo apt-get -y update
sudo apt-get -y install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo gpg --dearmor -o /etc/apt/ke>
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up Docker's APT repository:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://d>
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update

# Install Docker
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-com>

# User settings
nano .env
echo 'User settings saved to ".env"'

# Build the RPi image
sudo docker build driver/Dockerfile-rpi -f rpi powmr-driver

# Enable Docker service on startup
sudo systemctl enable docker

# Run detatched
sudo docker compose up -d