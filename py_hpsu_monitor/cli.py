import asyncio
from pathlib import Path
from typing import Optional

import tomlkit
import typer

from .commands.parse_candump import run_parse_candump
from .commands.monitor_canbus import run_monitor_canbus

app = typer.Typer()


@app.command()
def run(
    can_interface: str = typer.Option("can0", help="CAN bus interface to monitor"),
    config_file: Optional[Path] = typer.Option(None),
    log_frames: bool = typer.Option(False, "--log-frames"),
    log_registers: bool = typer.Option(False, "--log-registers"),
):
    if config_file and config_file.is_file():
        config = tomlkit.parse(config_file.read_text())
    else:
        config = {
            "registers": [
                {
                    "elster_index": 0x000E,
                    "interval": 30,
                    "receiver": 0x180,
                    "sender": 0x680,
                },
                {
                    "elster_index": 0x01D6,
                    "interval": 30,
                    "receiver": 0x180,
                    "sender": 0x680,
                },
                {
                    "elster_index": 0x091C,
                    "interval": 30,
                    "receiver": 0x180,
                    "sender": 0x680,
                },
                {
                    "elster_index": 0xC0F9,
                    "interval": 30,
                    "receiver": 0x180,
                    "sender": 0x680,
                },
            ]
        }

    asyncio.run(
        run_monitor_canbus(
            can_interface=can_interface,
            log_frames=log_frames,
            log_registers=log_registers,
            polling_configurations=config["registers"],
        )
    )


@app.command()
def parse_candump():
    asyncio.run(run_parse_candump())
