import asyncio

import typer

from .commands.parse_candump import run_parse_candump

app = typer.Typer()


@app.command()
def run():
    pass
    # asyncio.run(run_monitor_canbus())


@app.command()
def parse_candump():
    asyncio.run(run_parse_candump())
