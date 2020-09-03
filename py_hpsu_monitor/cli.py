import asyncio

import can
import typer
import ctypes
from .elster_protocol.elster_frame import (  # pylint: disable=relative-beyond-top-level
    ElsterFrame,
)

app = typer.Typer()


@app.command()
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_messages())
    loop.close()


async def print_messages():
    log_reader = can.CanutilsLogReader("contrib/candump-2020-09-01_233648.log")

    for message in log_reader:
        typer.echo(str(parse_elster_frame(message)))


def parse_elster_frame(message: can.Message):
    sender = message.arbitration_id
    data = message.data
    receiver = (data[0] & 0xF0) * 8 + (data[1] & 0x0F)
    type = data[0] & 0x0F
    value = None
    if data[2] == 0xFA:
        # extension telegram
        elster_index = ((data[3] & 0xFF) << 8) | (data[4] & 0xFF)
        if len(data) == 7:
            value = ctypes.c_int16(((data[5] & 0xFF) << 8) | (data[6] & 0xFF)).value
    else:
        elster_index = data[2]
        if len(data) >= 5:
            value = ctypes.c_int16(((data[3] & 0xFF) << 8) | (data[4] & 0xFF)).value

    return ElsterFrame(
        sender=sender,
        receiver=receiver,
        type=type,
        elster_index=elster_index,
        value=value,
    )
