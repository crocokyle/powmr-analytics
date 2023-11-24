import datetime

from driver.database import Database
from expected import EXPECTED

# TODO: Use pytest properly


INFLUX_ORG = "PowMr"
BUCKET = "solar_data"
API_KEY = "wc6WvzhFyekZIGpQDDKFKeDPFmPYQN47x6Bb1yTY6lLiIYoMB1YIFY9lNUjeTLGWoD17oRilr6ut8RPAWwEDxg=="

# Hardcoded container vars in docker-compose.yaml
INFLUX_HOST = '127.0.0.1'
INFLUX_PORT = 80
COM_PORT = '/dev/ttyUSB0'

DB = Database(
    api_key=API_KEY,
    ip=INFLUX_HOST,
    port=INFLUX_PORT,
    org=INFLUX_ORG,
    bucket=BUCKET,
    use_ssl=False,
    verify_ssl=False
)


def test_influxdb_push(response: dict[str], database: Database = DB) -> None:

    influx_record = {
        "measurement": "Power Statistics",
        "fields": response,
        'time': datetime.datetime.now().astimezone(datetime.timezone.utc)
    }

    database.write_api.write(
        database.bucket,
        database.org,
        record=influx_record,
        record_measurement_name="Power Statistics",
    )


if __name__ == "__main__":
    test_influxdb_push(response=EXPECTED)