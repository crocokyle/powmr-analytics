import logging
import os

import dotenv
from rich.logging import RichHandler

from driver.connection import PowMrConnection
from driver.database import Database
from driver.main import poll

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = RichHandler(markup=True, rich_tracebacks=True, log_time_format='[%m/%d/%y %H:%M:%S:%f]')
handler.setFormatter(logging.Formatter("{message}", style='{'))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


def main_loop(db: Database, inv_connection: PowMrConnection, max_retries=10):
    poll_attempts = 0
    push_attempts = 0
    while True:
        if (poll_attempts > max_retries) or (push_attempts > max_retries):
            failure = "poll inverter combo" if (poll_attempts > max_retries) else "update InfluxDB"
            raise Exception(f"Failed to {failure} after the maximum number of retries ({max_retries}).")
        try:
            dataframe = poll(inv_connection)
            log.info(f'Polled Solar All-in-one.')
            log.debug(dataframe.to_dict('records'))
            poll_attempts = 0
            try:
                db.write_api.write(
                    db.bucket,
                    db.org,
                    record=dataframe,
                    data_frame_measurement_name="Power Statistics",
                    data_frame_timestamp_column="timestamp"
                )
                log.info(f'Updated InfluxDB.')
                push_attempts = 0
            except Exception:
                push_attempts += 1
                log.exception(f'Failed to update InfluxDB.')
        except Exception:
            poll_attempts += 1
            log.exception(f"Failed to reach inverter combo.")


if __name__ == '__main__':
    dotenv.load_dotenv()

    API_KEY = os.environ['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']
    BUCKET = os.environ['DOCKER_INFLUXDB_INIT_BUCKET']
    INFLUX_ORG = os.environ['DOCKER_INFLUXDB_INIT_ORG']

    # Hardcoded container vars in docker-compose.yaml
    INFLUX_HOST = 'influxdb'
    INFLUX_PORT = 8086
    COM_PORT = '/dev/ttyUSB0'

    database = Database(
        api_key=API_KEY,
        ip=INFLUX_HOST,
        port=INFLUX_PORT,
        org=INFLUX_ORG,
        bucket=BUCKET,
        use_ssl=False,
        verify_ssl=False
    )

    inverter_connection = PowMrConnection(COM_PORT)

    main_loop(database, inverter_connection)
