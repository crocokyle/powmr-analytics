import datetime
from pprint import pprint
from typing import Any

import pandas as pd

from driver.commands import PowMrCommands, DerivedCommands
from driver.connection import PowMrConnection


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


def poll(connection: PowMrConnection, poll_count: int = 10):
    df = pd.DataFrame()

    while len(df) < poll_count:
        results = run_commands(connection)

        # Not sure why this is necessary. Draw value jumps up when charging and vice-versa
        if results['BATTERY_CHARGE_A'] > 0:
            results['BATTERY_DRAW_A'] = float(0)
            results['BATTERY_DRAW_W'] = float(0)

        if results['BATTERY_DRAW_A'] > 0:
            results['BATTERY_CHARGE_A'] = float(0)
            results['BATTERY_CHARGE_W'] = float(0)

        results['timestamp'] = datetime.datetime.now().astimezone(datetime.timezone.utc)
        new = pd.DataFrame(results, index=[results['timestamp']])
        df = pd.concat([df, new])

    return df


if __name__ == "__main__":
    df = poll()
    pprint(df)