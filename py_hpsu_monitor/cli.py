import asyncio

import typer

from .commands.parse_candump import run_parse_candump
from .commands.monitor_canbus import run_monitor_canbus

app = typer.Typer()


@app.command()
def run():
    asyncio.run(run_monitor_canbus())


@app.command()
def parse_candump():
    asyncio.run(run_parse_candump())
