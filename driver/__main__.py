import datetime
from pprint import pprint
from typing import Any
import time
import pandas as pd

from driver.commands import PowMrCommands
from driver.connection import PowMrConnection


def run_commands(connection) -> dict[str, Any]:
    results = {}
    run_registers = []
    for command in PowMrCommands:
        force_update = False if command.register in run_registers else True
        results[str(command)] = connection.read_register(command, force_update=force_update)
        run_registers.append(command.register)

    return results


def poll(connection: PowMrConnection, poll_count: int = 10):
    df = pd.DataFrame()

    while len(df) < poll_count:
        results = run_commands(connection)
        if results['BATTERY_CHARGE_CURRENT_A'] > 0: # Not sure why this is necessary. Draw value jumps up to 6544.
            results['BATTERY_DRAW_CURRENT_A'] = float(0)
        results['timestamp'] = datetime.datetime.now().astimezone(datetime.timezone.utc)
        new = pd.DataFrame(results, index=[results['timestamp']])
        df = pd.concat([df, new])

    return df


if __name__ == "__main__":
    df = poll()
    pprint(df)