import datetime

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class Database:
    def __init__(self, api_key, ip, port, org, bucket, use_ssl, verify_ssl):
        self.api_key: str = api_key
        self.ip: str = ip
        self.port = int(port)
        self.org: str = org
        self.use_ssl: bool = use_ssl
        self.verify_ssl: bool = verify_ssl

        self.bucket = bucket
        self.protocol = "https" if use_ssl else "http"
        self.uri = f'{self.protocol}://{self.ip}:{self.port}'
        self.client = InfluxDBClient(url=self.uri, token=self.api_key, org=self.org, verify_ssl=self.verify_ssl)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def write_results(self, responses: dict[str]):
        influx_record = {
            "measurement": "Power Statistics",
            "fields": responses,
            'time': datetime.datetime.now().astimezone(datetime.timezone.utc)
        }

        self.write_api.write(
            self.bucket,
            self.org,
            record=influx_record,
            record_measurement_name="Power Statistics",
        )

    def read_data(self):
        # using Table structure
        tables = self.query_api.query(f'from(bucket:"{self.bucket}") |> range(start: -10m)')
        for table in tables:
            print(table)
            for row in table.records:
                print(row.values)


if __name__ == '__main__':
    ...
