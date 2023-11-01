from driver.connection import PowMrConnection
from driver.commads import PowMrCommands

if __name__ == "__main__":
    connection = PowMrConnection("COM4")

    # Thermal Shit
    ac_temp = int(connection.read_register(PowMrCommands.AC_TEMP))/10
    dc_temp = int(connection.read_register(PowMrCommands.DC_TEMP))/10
    tr_temp = int(connection.read_register(PowMrCommands.TR_TEMP))/10

    # Grid Power
    grid_current = connection.read_register(PowMrCommands.CURRENT_VA)

    # Usage
    total_power = connection.read_register(PowMrCommands.TOTAL_POWER_CONSUMPTION)
    total_kwh = int(total_power)/10
    current_power = connection.read_register(PowMrCommands.CURRENT_POWER)
    current_voltage = int(connection.read_register(PowMrCommands.CURRENT_VOLTAGE))/10
    current_current = int(connection.read_register(PowMrCommands.CURRENT_CURRENT))/10
    current_va = connection.read_register(PowMrCommands.CURRENT_VA)

    # Battery
    battery_voltage = int(connection.read_register(PowMrCommands.BATTERY_VOLTAGE))/10
    battery_charge = int(connection.read_register(PowMrCommands.BATTERY_SOC))

    print(f'{"=" * 10} Thermal Statistics {"=" * 10}')
    print(f"DC Temperature: {dc_temp} °C")
    print(f"AC Temperature: {ac_temp} °C")
    print(f"Transformer Rectifier Temperature: {tr_temp} °C")
    print(f'{"="*10} Power Consumption {"="*10}')
    print(f"Total: {total_kwh} kWh")
    print(f"Current Voltage: {current_voltage} VAC")
    print(f"Currently Using: {current_current} A")
    print(f"Currently Using: {current_power} W")
    print(f"Currently Using: {current_va} VA")
    print(f'{"=" * 10} Battery {"=" * 10}')
    print(f"Battery Voltage: {battery_voltage} VDC")
    print(f"Battery Charge: {battery_charge}%")
    print(f'{"=" * 10} Grid Power {"=" * 10}')


