# powmr-analytics
Pulls data from PowMr All-In-One inverters via MODBUS and visualizes the data via InfluxDB. This project was designed 
to run on a Raspberry Pi.
![image](https://github.com/crocokyle/powmr-analytics/assets/11140843/e86a8dfe-16fc-4057-8066-949280cebeb0)

## Prerequisites

> ⚠️ At the moment powmr-analytics does not run on Windows due to 
> [an issue forwarding COM ports](https://github.com/docker/for-win/issues/1018)
> into a Docker container. There may be unsupported workarounds using WSL or a hypervisor to host Docker but these 
> have not been tested.

- A PowMR Inverter with a serial connection to your Docker host
- A Linux host with [Docker installed](https://docs.docker.com/engine/install/)
- *Optional:* ch340 drivers are generally preinstalled on Linux. [The ch340 drivers](driver/ch340_drivers) only need 
  to be installed if you are using a USB connection on an OS that doesn't include them. Running `sudo dmesg | grep 
  ttyUSB*` should show you if they are preinstalled.
## Configuration

Configure settings before spinning up the services by modifying `.env`:
- Set the `COM_PORT` variable to the COM port (on your Docker host) that is connected to your PowMr inverter.
  - You can enumerate connected USB devices by running `sudo dmesg | grep ttyUSB*` 
  - Example Value: `/dev/ttyUSB0`
- ⚠️ If publicly exposing this service, change the default credentials for InfluxDB
  - To generate a new API key, exec into the InfluxDB container and run:
  
    `influx auth create -o <INFLUXDB-ORG-NAME-IN-.ENV> --all-access`


## Installation

- `docker compose up` or `docker compose up -d` for detached
- Browse to `http://<your-docker-host-ip>`

## Raspberry Pi Instructions

- Install Raspberry Pi OS (32-bit) (Yes 32-bit even on the Pi 4)
- Connect to the Raspberry Pi physically or via SSH 
- Clone this repo to your raspberry pi: `git clone https://github.com/crocokyle/powmr-analytics.git`
- Set the installer permissions to executable: `sudo chmod +x setup-rpi.sh`
- Run `./setup-rpi.sh`