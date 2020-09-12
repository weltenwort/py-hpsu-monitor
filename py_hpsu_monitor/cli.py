import asyncio
from pathlib import Path
from py_hpsu_monitor.config import (
    load_configuration_from_file_path,
    load_default_configuration,
)
from typing import Optional

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
    configuration = (
        load_configuration_from_file_path(config_file)
        if config_file
        else load_default_configuration()
    )

    asyncio.run(
        run_monitor_canbus(
            can_interface=can_interface,
            log_frames=log_frames,
            log_registers=log_registers,
            mqtt_config=configuration.mqtt,
            polling_configurations=configuration.can_bus.polling_configuration,
            sender_id=configuration.can_bus.sender_id,
        )
    )


@app.command()
def parse_candump():
    asyncio.run(run_parse_candump())
