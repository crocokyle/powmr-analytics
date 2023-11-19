## InfluxDB Configuration

There are two files used to configure the InfluxDB instance:

- `influxdb/config.json` - Used for basic InfluxDB config settings
- `CONFIG.env` - Used to bypass the user configuration setup screen using defaults
  - Modify this to change credentials for the database. The driver will read from this .env file to get access to 
    the database.
  - When updating the org, a new API is required. To generate, exec into the InfluxDB container and run `influx auth 
    create -o <NEW-ORG-NAME> --all-access`
  - Set `EXTERNAL_LISTEN_PORT` to the port you'd like your host machine to listen on.