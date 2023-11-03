from enum import Enum
from typing import Any


class PowMrCommand(Enum):
    def __init__(self, address, register, count, divisor=None):
        self.address = address
        self.register = register
        self.count = count
        self.divisor = divisor
        self.registers = {}
        self.last_value: Any = None

    def __add__(self, other):
        try:
            return float(self.last_value) + float(other.last_value)
        except TypeError:
            return None

    def __sub__(self, other):
        try:
            return float(self.last_value) - float(other.last_value)
        except TypeError:
            return None

    def __mul__(self, other):
        try:
            return float(self.last_value) * float(other.last_value)
        except TypeError:
            return None

    def __div__(self, other):
        try:
            return float(self.last_value) / float(other.last_value)
        except TypeError:
            return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return ""  # TODO: complete this


class PowMrCommands(PowMrCommand):
    # address, register, count, divisor (Optional)

    # Totals
    TOTAL_POWER_W = 61487, 11, 13, 10

    # Solar
    SOLAR_POWER_W = 256, 9, 15
    SOLAR_CURRENT_A = 256, 8, 15, 10
    SOLAR_VOLTAGE_VDC = 256, 7, 15, 10

    # Inverter
    INVERTER_POWER_W = 516, 23, 31
    INVERTER_VA = 516, 24, 31
    INVERTER_CURRENT_A = 516, 21, 31, 10
    INVERTER_VOLTAGE_VAC = 516, 18, 31, 10

    # Battery
    BATTERY_VOLTAGE_VDC = 256, 1, 15, 10
    BATTERY_SOC = 256, 0, 15
    BATTERY_CHARGE_A = 516, 26, 31, 10
    BATTERY_DRAW_A = 256, 2, 15, 10

    # Grid Power

    # Thermal Data
    DC_TEMP_C = 516, 28, 31, 10
    AC_TEMP_C = 516, 29, 31, 10
    TR_TEMP_C = 516, 30, 31, 10  # TRANSFORMER RECTIFIER


class DerivedCommand(Enum):
    def __init__(self, expression: str):
        self.expression = expression

    def __str__(self):
        return self.name


class DerivedCommands(DerivedCommand):
    BATTERY_DRAW_W = "PowMrCommands.BATTERY_DRAW_CURRENT_A * PowMrCommands.BATTERY_VOLTAGE_VDC"
    BATTERY_CHARGE_W = "PowMrCommands.BATTERY_CHARGE_CURRENT_A * PowMrCommands.BATTERY_VOLTAGE_VDC"
