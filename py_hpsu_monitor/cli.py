import asyncio

import can
import typer
from .elster_protocol.parse_can_message import (  # pylint: disable=relative-beyond-top-level
    parse_can_message,
)

app = typer.Typer()


@app.command()
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_messages())
    loop.close()


async def print_messages():
    log_reader = can.CanutilsLogReader("contrib/candump-2020-09-05_135811.log")

    for message in log_reader:
        typer.echo(f"{message} - {parse_can_message(message)}")
