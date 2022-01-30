# pyright: reportUnknownMemberType=warning
from datetime import datetime

import typer

from ..elster_protocol.elster_frame import ElsterReadRequestFrame, ElsterWriteFrame
from ..elster_protocol.create_can_message import create_can_message


generate_can_message_app = typer.Typer()


@generate_can_message_app.command(name="write")
def generate_write_message(
    elster_index: int,
    value: int,
    sender: int = typer.Option(default=0x680),
    receiver: int = typer.Option(0x180),
):
    frame = ElsterWriteFrame(
        timestamp=datetime.now().timestamp(),
        sender=sender,
        receiver=receiver,
        elster_index=elster_index,
        value=value,
    )
    can_message = create_can_message(frame)

    print(f"{hex(sender)[2:]}#{can_message.data.hex('.')}")


@generate_can_message_app.command(name="read-request")
def generate_read_request_message(
    elster_index: int,
    sender: int = typer.Option(0x680),
    receiver: int = typer.Option(0x180),
):
    frame = ElsterReadRequestFrame(
        timestamp=datetime.now().timestamp(),
        sender=sender,
        receiver=receiver,
        elster_index=elster_index,
    )
    can_message = create_can_message(frame)

    print(f"{hex(sender)[2:]}#{can_message.data.hex('.')}")
