import asyncio

import typer

from .commands.parse_candump import run_parse_candump
from .commands.monitor_canbus import run_monitor_canbus

app = typer.Typer()


@app.command()
def run(
    log_frames: bool = typer.Option(False, "--log-frames"),
    log_registers: bool = typer.Option(False, "--log-registers"),
):
    asyncio.run(run_monitor_canbus(log_frames=log_frames, log_registers=log_registers))


@app.command()
def parse_candump():
    asyncio.run(run_parse_candump())
