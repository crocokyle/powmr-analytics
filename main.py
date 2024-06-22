import asyncio
import datetime
import logging
import os

import dotenv

from database import Database
from drivers.bms.main import DalyBMSConnection
from drivers.inverter.connection import PowMrConnection
from drivers.inverter.main import get_results

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


async def main_loop(db: Database, inv_connection: PowMrConnection, bms_connection, max_retries=None):
    poll_attempts = 0
    push_attempts = 0
    last_poll = datetime.datetime.now()
    while True:
        if max_retries is not None and ((poll_attempts > max_retries) or (push_attempts > max_retries)):
            failure = "poll inverter combo" if (poll_attempts > max_retries) else "update InfluxDB"
            raise Exception(f"Failed to {failure} after the maximum number of retries ({max_retries}).")
        try:
            results = get_results(inv_connection)
            bms_state = await bms_connection.get_state()
            results['BMS_SOC'] = bms_state.get('soc_percent')
            results['BMS_VDC'] = bms_state.get('total_voltage')
            results['BMS_CURRENT_A'] = bms_state.get('current')
            delta = datetime.datetime.now() - last_poll
            last_poll = datetime.datetime.now()
            log.info(f'Polled Solar All-in-one.')

            results['SOLAR_kWh'] = (delta.total_seconds() / 3600) * (results['SOLAR_POWER_W'] / 1000)
            results['USAGE_kWh'] = (delta.total_seconds() / 3600) * (results['INVERTER_POWER_W'] / 1000)

            log.debug(results)
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

    # Daly BMS
    DALY_BMS_MAC = os.environ['DALY_BMS_MAC']

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
    bms_connection = DalyBMSConnection(mac=DALY_BMS_MAC)

    asyncio.run(main_loop(database, inverter_connection, bms_connection))
