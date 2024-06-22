import asyncio
import logging

from bleak.exc import BleakDeviceNotFoundError

from .dalybms import DalyBMSBluetooth

logger = logging.getLogger(__name__)


class DalyBMSConnection:
    def __init__(self, mac: str = "17:71:06:02:08:91"):
        self.client = DalyBMSBluetooth(logger=logger)
        self.mac = mac
        self.connected = False

    async def connect(self):
        await self.client.connect(mac_address="17:71:06:02:08:91")
        self.connected = True

    async def disconnect(self):
        await self.client.disconnect()
        self.connected = False

    async def get_state(self):
        try:
            if not self.connected:
                await self.connect()
            soc = await self.client.get_soc()
            logger.debug(soc)
            if not soc:
                logger.warning("failed to receive SOC")
                return
            logger.info(soc)
            await self.disconnect()
            return soc
        except Exception as e:
            logger.warning(e)

async def main():
    bms = DalyBMSConnection(mac="17:71:06:02:08:91")

    attempts = 0
    while attempts < 100:
        try:
            await bms.get_state()
        except BleakDeviceNotFoundError:
            attempts += 1
            print(f'Attempt {attempts} failed')


if __name__ == "__main__":
    asyncio.run(main())
