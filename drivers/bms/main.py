import asyncio
import logging

from bleak.exc import BleakDeviceNotFoundError

from drivers.bms.dalybms import DalyBMSBluetooth

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class DalyBMSConnection:
    def __init__(self, mac: str = "17:71:06:02:08:91"):
        self.client = DalyBMSBluetooth(logger=log)
        self.mac = mac
        self.connected = False

    async def connect(self):
        log.info("Connecting to BMS via Bluetooth...")
        await self.client.connect(mac_address="17:71:06:02:08:91")
        self.connected = True
        log.info("BMS connection established")

    async def disconnect(self):
        await self.client.disconnect()
        self.connected = False
        log.info("BMS disconnected")

    async def get_state(self):
        try:
            if not self.connected:
                await self.connect()
            soc = await self.client.get_soc()
            if not soc:
                log.warning("failed to receive SOC")
                return
            log.info(soc)
            await self.disconnect()
            return soc
        except Exception as e:
            log.warning(e)


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
