from pymodbus.client import ModbusSerialClient
from pymodbus.framer import ModbusRtuFramer

from drivers.inverter.commands import PowMrCommand


class PowMrConnection:
    def __init__(self, port, framer=ModbusRtuFramer, baudrate=9600, bytesize=8, parity="N", stopbits=1):
        self.port = port
        self.framer = framer
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits

        self.client = ModbusSerialClient(
            port=self.port,
            framer=self.framer,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits
        )

    def connect(self):
        self.client.connect()

    def read_register(self, command: PowMrCommand, force_update=False):
        if force_update or (command.register not in command.registers):
            result = self.client.read_holding_registers(command.address, command.count, 1).registers
        else:
            result = command.registers
        for register, value in enumerate(result):
            command.registers[register] = value

        if command.divisor:
            value = int(result[command.register]) / command.divisor
        else:
            value = int(result[command.register])

        command.last_value = value

        return value

    def close(self):
        self.client.close()
