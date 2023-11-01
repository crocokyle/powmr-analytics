from typing import Any

class PowMrCommand:
    def __init__(self, address, register, count):
        self.address: int = address
        self.register: int = register
        self.count: int = count
        self.registers: dict[int, Any] = {}

    def __repr__(self):
        return ""  # TODO: complete this


class PowMrCommands:
    # Usage
    TOTAL_POWER_CONSUMPTION = PowMrCommand(61487, 11, 13)
    CURRENT_POWER = PowMrCommand(516, 23, 31)
    CURRENT_VA = PowMrCommand(516, 24, 31)
    CURRENT_CURRENT = PowMrCommand(516, 21, 31)
    CURRENT_VOLTAGE = PowMrCommand(516, 18, 31)

    # Battery
    BATTERY_VOLTAGE = PowMrCommand(256, 1, 15)
    BATTERY_SOC = PowMrCommand(256, 0, 15)

    # Grid Power
    GRID_CURRENT = PowMrCommand(516, 26, 31)

    # Thermal Data
    DC_TEMP = PowMrCommand(516, 28, 31)
    AC_TEMP = PowMrCommand(516, 29, 31)
    TR_TEMP = PowMrCommand(516, 30, 31)  # TRANSFORMER RECTIFIER
