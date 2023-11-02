import logging
import os
import sys

import dotenv

from database.__main__ import Database
from driver.__main__ import poll
from driver.connection import PowMrConnection

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


def main_loop(db: Database, inv_connection: PowMrConnection):
    while True:
        dataframe = poll(inv_connection)
        log.info(f'Polled Solar All-in-one:\n{dataframe.to_string()}')
        db.write_api.write(
            db.bucket,
            db.org,
            record=dataframe,
            data_frame_measurement_name="Power Statistics",
            data_frame_timestamp_column="timestamp"
        )
        log.info(f'Updated InfluxDB at {dataframe["timestamp"][1]}')


if __name__ == '__main__':
    dotenv.load_dotenv()

    API_KEY = os.environ['API_KEY']
    BUCKET = os.environ['BUCKET']
    INFLUX_HOST = os.environ['INFLUX_HOST']
    INFLUX_PORT = os.environ['INFLUX_PORT']
    INFLUX_ORG = os.environ['INFLUX_ORG']

    database = Database(
        api_key=API_KEY,
        ip=INFLUX_HOST,
        port=INFLUX_PORT,
        org=INFLUX_ORG,
        bucket=BUCKET,
        use_ssl=True,
        verify_ssl=False
    )

    inverter_connection = PowMrConnection("COM4")

    main_loop(database, inverter_connection)
