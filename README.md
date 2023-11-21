# powmr-analytics
Pulls data from PowMr All-In-One inverters via MODBUS and visualizes the data via InfluxDB
![image](https://github.com/crocokyle/powmr-analytics/assets/11140843/e86a8dfe-16fc-4057-8066-949280cebeb0)

> ⚠️ At the moment powmr-analytics does not run on Windows due to 
> [an issue with forwarding COM ports](https://github.com/docker/for-win/issues/1018)
> into a Docker container.

## Prerequisites
- A PowMR Inverter with a serial connection to your Docker host
- A Linux host running Docker
- If using a USB connection, you'll need the [ch340 driver](driver/ch340_drivers).

## Configuration

Configure settings before spinning up the services by modifying `.env`:
- Set the `COM_PORT` variable to the COM port (on your Docker host) that is connected to your PowMr inverter.
  - You can enumerate connected USB devices by running `sudo dmesg | grep ttyUSB*` 
  - Example Value: `/dev/ttyS5`
- ⚠️ If publicly exposing this service, change the default credentials for InfluxDB
  - To generate a new API key, exec into the InfluxDB container and run:
  
    `influx auth create -o <INFLUXDB-ORG-NAME-IN-.ENV> --all-access`


## Installation

- `docker compose up` or `docker compose up -d` for detached
- Browse to `http://<your-docker-host-ip>`


