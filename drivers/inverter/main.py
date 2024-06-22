from pprint import pprint
from typing import Any

from drivers.inverter.commands import PowMrCommands, DerivedCommands
from drivers.inverter.connection import PowMrConnection


def run_commands(connection) -> dict[str, Any]:
    results = {}
    run_registers = []
    for command in PowMrCommands:
        force_update = False if command.register in run_registers else True
        results[str(command)] = connection.read_register(command, force_update=force_update)
        run_registers.append(command.register)

    for command in DerivedCommands:
        results[str(command)] = eval(command.expression)

    return results


def get_results(connection: PowMrConnection) -> dict[str, Any]:
    """Gets and corrects fields based on weird PowMr Logic"""
    results = run_commands(connection)

    # TODO: There's a lot more weirdness in these fields...values multiply in certain scenarios
    # Not sure why this is necessary. Draw value jumps up when charging and vice-versa
    if results['BATTERY_CHARGE_A'] > 0:
        results['BATTERY_DRAW_A'] = float(0)
        results['BATTERY_DRAW_W'] = float(0)

    if results['BATTERY_DRAW_A'] > 0:
        results['BATTERY_CHARGE_A'] = float(0)
        results['BATTERY_CHARGE_W'] = float(0)

    return results


if __name__ == "__main__":
    df = get_results()
    pprint(df)
