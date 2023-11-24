import datetime
import logging
import os

import dotenv
from rich.logging import RichHandler

from driver.connection import PowMrConnection
from driver.database import Database
from driver.main import get_results

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = RichHandler(markup=True, rich_tracebacks=True, log_time_format='[%m/%d/%y %H:%M:%S:%f]')
handler.setFormatter(logging.Formatter("{message}", style='{'))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


def main_loop(db: Database, inv_connection: PowMrConnection, max_retries=None):
    poll_attempts = 0
    push_attempts = 0
    last_poll = datetime.datetime.now()
    while True:
        if max_retries is not None and ((poll_attempts > max_retries) or (push_attempts > max_retries)):
            failure = "poll inverter combo" if (poll_attempts > max_retries) else "update InfluxDB"
            raise Exception(f"Failed to {failure} after the maximum number of retries ({max_retries}).")
        try:
            delta = datetime.datetime.now() - last_poll
            results = get_results(inv_connection)
            last_poll = datetime.datetime.now()
            log.info(f'Polled Solar All-in-one.')

            results['fields']['SOLAR_kWh'] = ((delta.total_seconds() / 3600) *
                                              (results['fields']['SOLAR_POWER_W'] / 1000))
            results['fields']['USAGE_kWh'] = ((delta.total_seconds() / 3600) *
                                              (results['fields']['INVERTER_POWER_W'] / 1000))

            log.debug(results.get('fields'))
            poll_attempts = 0
            try:
                db.write_results(results)
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
