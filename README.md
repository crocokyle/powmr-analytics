# powmr-analytics
Pulls data from PowMr All-In-One inverters via MODBUS and visualizes the data via InfluxDB
![image](https://github.com/crocokyle/powmr-analytics/assets/11140843/e86a8dfe-16fc-4057-8066-949280cebeb0)

## Installation
> ⚠️ At the moment powmr-analytics does not run on Windows due to 
> [an issue with forwarding COM ports](https://github.com/docker/for-win/issues/1018)
> into a Docker container.

- Install [the appropriate ch340 driver](driver/ch340_drivers).
- `docker compose up`
- Browse to `http://<your-docker-host-ip>`


## Configuration

Configure settings by modifying `.env`:
- ⚠️ If publicly exposing this service, change the default credentials for InfluxDB
  - To generate a new API key, exec into the InfluxDB container and run `influx auth 
    create -o <NEW-ORG-NAME> --all-access`
- Specify the COM port address you want to use from your docker host.
  - Example: `/dev/ttyS5`